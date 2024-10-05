import dataclasses as dc
import logging
import typing as t
import uuid

import chromadb
from chromadb.errors import ChromaError
from llama_index.core import Document
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.node_parser import SemanticSplitterNodeParser

from wiki_helper.storing.storage import Storage, StorageError

logger = logging.getLogger(__name__)


@dc.dataclass(frozen=True)
class VectorStorageConnection:
    host: str
    port: int


class VectorStorage(Storage[str, t.Sequence[str]]):
    def __init__(
        self,
        embedding_builder: BaseEmbedding,
        connection_settings: VectorStorageConnection,
    ) -> None:
        self.__embedding_function = embedding_builder
        self.__num_neighbors = 5
        self.__chroma_client = chromadb.HttpClient(
            host=connection_settings.host, port=connection_settings.port
        )
        self.__collection_name = uuid.uuid4().hex
        self.__splitter = SemanticSplitterNodeParser(
            buffer_size=25,
            breakpoint_percentile_threshold=80,
            embed_model=self.__embedding_function,
        )

    def store(self, content: str) -> None:
        try:
            logger.info("Storing content in vector storage.")
            chroma_collection = self.__chroma_client.get_or_create_collection(
                self.__collection_name
            )

            if not self.__collection_is_empty():
                logger.info(f"Updating existing collection: {self.__collection_name}")
            else:
                logger.info(f"Storing in a new collection: {self.__collection_name}")

            document = Document(text=content)
            nodes = self.__splitter.get_nodes_from_documents([document])

            texts = [node.get_content() for node in nodes]

            embeddings = self.__embedding_function.get_text_embedding_batch(texts)

            chroma_collection.add(
                documents=texts,
                embeddings=embeddings,
                ids=[uuid.uuid4().hex for _ in texts],
            )
            logger.info("Content successfully stored in vector storage.")

        except ChromaError as error:
            raise StorageError(
                f"Failed to store content due to error '{error}'"
            ) from error

    def get(self, query: str) -> t.Sequence[str]:
        try:
            logger.info(f"Retrieving content for query: {query}")
            chroma_collection = self.__chroma_client.get_or_create_collection(
                self.__collection_name,
            )

            query_embedding = self.__embedding_function.get_query_embedding(query)

            results = chroma_collection.query(
                query_embeddings=query_embedding, n_results=self.__num_neighbors
            )
            if results["documents"] is None:
                logger.info("No results found for the query.")
                raise StorageError("No results found")

            flat_documents = [
                document
                for subdocuments in results["documents"]
                for document in subdocuments
            ]

            logger.info(f"Retrieved {len(flat_documents)} documents for the query.")
            return [str(flat_document) for flat_document in flat_documents]

        except ChromaError as error:
            raise StorageError(
                f"Failed to get content due to error '{error}'"
            ) from error

    def clear(self) -> None:
        try:
            logger.info("Clearing vector storage collection.")
            self.__chroma_client.delete_collection(self.__collection_name)
            logger.info("Vector storage collection cleared.")
        except ChromaError as error:
            raise StorageError(
                f"Failed to clear collection due to error '{error}'"
            ) from error

    def __collection_is_empty(self) -> bool:
        chroma_collection = self.__chroma_client.get_or_create_collection(
            self.__collection_name
        )
        count = chroma_collection.count()
        logger.debug(f"Collection {self.__collection_name} contains {count} items.")
        return count == 0
