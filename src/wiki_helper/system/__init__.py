# import pathlib as pth

# from llama_index.core.base.embeddings.base import BaseEmbedding
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# from wiki_helper.configuration import Configuration
# from wiki_helper.knowledge_base.impl.knowledge_base import ExternalKnowledgeBase
# from wiki_helper.rag.impl.generative_model import LargeLanguageModel
# from wiki_helper.storing.impl.storage import VectorStorage, VectorStorageConnection
# from wiki_helper.system.impl.rag_system import RagSystemImpl
# from wiki_helper.system.rag_system import RagSystem


# def build_embedding_creator(embedder_location: pth.Path) -> BaseEmbedding:
#     prompt_for_retrieval = "Represent this sentence for searching relevant passages:"

#     return HuggingFaceEmbedding(
#         model_name=embedder_location.as_posix(),
#         query_instruction=prompt_for_retrieval,
#     )


# def build_system(configuration: Configuration) -> RagSystem:
#     return RagSystemImpl(
#         generator=LargeLanguageModel(model_location=configuration.model_location),
#         knowledge_base=ExternalKnowledgeBase(configuration.language),
#         storage=VectorStorage(
#             embedding_builder=build_embedding_creator(configuration.embedder_location),
#             connection_settings=VectorStorageConnection(
#                 host=configuration.storage_host, port=configuration.storage_port
#             ),
#         ),
#     )
