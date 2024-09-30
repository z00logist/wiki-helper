import wikipediaapi
from yarl import URL

from wiki_helper.qna.knowledge_base import KnowledgeBase, KnowledgeBaseError


class ExternalKnowledgeBase(KnowledgeBase[URL, str]):
    def __init__(self, language_code: str) -> None:
        self.__parser = wikipediaapi.Wikipedia(
            user_agent="wiki-helper",
            language=language_code,
            extract_format=wikipediaapi.ExtractFormat.WIKI,
        )

    def get_content(self, url: URL) -> str:
        title = url.parts[-1]

        parsed_content = self.__parser.page(title)

        if len(parsed_content.text) == 0:
            raise KnowledgeBaseError(
                f"The page '{title}' does not exist on Wikipedia. Please check the correctness of the provided URL."
            )

        return str(parsed_content.text)
