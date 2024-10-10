import logging
import typing as t

from yarl import URL

from wiki_helper.qna.generative_model import GenerativeModel, GenerativeModelError
from wiki_helper.qna.impl.generative_model import QnAContext
from wiki_helper.qna.knowledge_base import KnowledgeBase, KnowledgeBaseError
from wiki_helper.qna.system import RagSystem, RagSystemError
from wiki_helper.storing.storage import Storage, StorageError

logger = logging.getLogger(__name__)


class StreamingRagSystem(RagSystem[t.Iterator[str]]):
    def __init__(
        self,
        generator: GenerativeModel[QnAContext, t.Iterator[str]],
        knowledge_base: KnowledgeBase[URL, str],
        storage: Storage[str, t.Sequence[str]],
    ) -> None:
        self.__generator = generator
        self.__storage = storage
        self.__knowledge_base = knowledge_base

    def train(self, location: URL) -> None:
        logger.info(f"Training started with url: '{location}'")
        try:
            content = self.__knowledge_base.get_content(location)

            logger.debug(
                f"Content retrieved from knowledge base for '{location}': content length -- {len(content)}."
            )

            self.__storage.store(content)

            logger.info("Content successfully stored.")
        except (KnowledgeBaseError, StorageError) as error:
            raise RagSystemError(
                f"Failed to train QnA System due to error '{error}'"
            ) from error

    def answer(self, query: str) -> t.Iterator[str]:
        logger.info(f"Answering query: '{query}'")

        if len(query) == 0:
            logger.warning("Empty query received.")

            yield "Sorry, I can't help you with an empty query."

            return
        try:
            context = self.__storage.get(query)

            logger.debug(f"Retrieved context for query: '{context}'")

            for token in self.__generator.generate(
                QnAContext(query=query, context=context)
            ):
                yield token

        except (StorageError, GenerativeModelError) as error:
            raise RagSystemError(
                f"Failed to answer question due to error '{error}'"
            ) from error

    def delete(self) -> None:
        logger.info("Deleting QnA System data.")
        try:
            self.__storage.clear()

            logger.info("QnA System successfully deleted.")

        except StorageError as error:
            raise RagSystemError(
                f"Failed to delete QnA System due to error '{error}'"
            ) from error
