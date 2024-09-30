import typing as t

from yarl import URL

from wiki_helper.qna.knowledge_base import KnowledgeBase, KnowledgeBaseError
from wiki_helper.qna.generative_model import GenerativeModel, GenerativeModelError
from wiki_helper.qna.impl.generative_model import QnAContext
from wiki_helper.storing.storage import Storage, StorageError
from wiki_helper.qna.rag_system import RagSystem, RagSystemError


class RagSystemImpl(RagSystem):
    def __init__(
        self,
        generator: GenerativeModel[QnAContext],
        knowledge_base: KnowledgeBase[URL, str],
        storage: Storage[str, t.Sequence[str]],
    ) -> None:
        self.__generator = generator
        self.__storage = storage
        self.__knowledge_base = knowledge_base

    def train(self, location: URL) -> None:
        try:
            content = self.__knowledge_base.get_content(location)
            self.__storage.store(content)
        except (KnowledgeBaseError, StorageError) as error:
            raise RagSystemError(
                f"Failed to train QnA System due to error '{error}'"
            ) from error

    def answer(self, query: str) -> str:
        if len(query) == 0:
            return "Sorry, I can't help you with an empty query."
        try:
            context = self.__storage.get(query)

            return self.__generator.generate(QnAContext(query=query, context=context))

        except (StorageError, GenerativeModelError) as error:
            raise RagSystemError(
                f"Failed to answer question due to error '{error}'"
            ) from error
