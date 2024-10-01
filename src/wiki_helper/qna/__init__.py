import pathlib as pth

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from wiki_helper.configuration import Configuration
from wiki_helper.qna.impl.generative_model import LargeLanguageModel
from wiki_helper.qna.impl.knowledge_base import ExternalKnowledgeBase
from wiki_helper.qna.impl.system import RagSystemImpl
from wiki_helper.qna.system import RagSystem
from wiki_helper.storing.impl.storage import VectorStorage, VectorStorageConnection


def build_embedding_creator(embedder_location: pth.Path) -> BaseEmbedding:
    prompt_for_retrieval = "Represent this sentence for searching relevant passages:"
    return HuggingFaceEmbedding(
        model_name=embedder_location.as_posix(),
        query_instruction=prompt_for_retrieval,
    )


def build_system(configuration: Configuration) -> RagSystem:
    return RagSystemImpl(
        generator=LargeLanguageModel(model_location=configuration.llm.location),
        knowledge_base=ExternalKnowledgeBase(configuration.language),
        storage=VectorStorage(
            embedding_builder=build_embedding_creator(configuration.embedder.location),
            connection_settings=VectorStorageConnection(
                host=configuration.storage.host, port=configuration.storage.port
            ),
        ),
    )
