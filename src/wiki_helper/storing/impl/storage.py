import dataclasses as dc
import typing as t
import uuid

import chromadb
from chromadb.errors import ChromaError
from llama_index.core import Document
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.node_parser import SemanticSplitterNodeParser

from wiki_helper.storing.storage import Storage, StorageError


@dc.dataclass(frozen=True)
class VectorStorageConnection:
    host: str
    port: int


class VectorStorage(Storage[str, t.Sequence[str]]):
    def __init__(
        self,
        embedding_builder: BaseEmbedding,
        connection_settings: VectorStorageConnection,
    ):
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
            chroma_collection = self.__chroma_client.get_or_create_collection(
                self.__collection_name
            )

            if not self.__collection_is_empty():
                print(f"Updating existing collection: {self.__collection_name}")
            else:
                print(f"Storing in a new collection: {self.__collection_name}")

            document = Document(text=content)

            nodes = self.__splitter.get_nodes_from_documents([document])

            texts = [node.get_content() for node in nodes]
            embeddings = self.__embedding_function.get_text_embedding_batch(texts)

            chroma_collection.add(
                documents=texts,
                embeddings=embeddings,
                ids=[uuid.uuid4().hex for _ in texts],
            )

        except ChromaError as error:
            raise StorageError(
                f"Failed to store content due to error '{error}'"
            ) from error

    def get(self, query: str) -> t.Sequence[str]:
        try:
            chroma_collection = self.__chroma_client.get_or_create_collection(
                self.__collection_name,
            )

            query_embedding = self.__embedding_function.get_query_embedding(query)

            results = chroma_collection.query(
                query_embeddings=query_embedding, n_results=self.__num_neighbors
            )
            if results["documents"] is None:
                raise StorageError("No results found")
            
            flat_documents = [document for subdocuments in results["documents"] for document in subdocuments]

            return [str(flat_document) for flat_document in flat_documents]

        except ChromaError as error:
            raise StorageError(
                f"Failed to get content due to error '{error}'"
            ) from error

    def __collection_is_empty(self) -> bool:
        chroma_collection = self.__chroma_client.get_or_create_collection(
            self.__collection_name
        )
        count = chroma_collection.count()
        return count == 0
