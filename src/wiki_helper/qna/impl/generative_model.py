import dataclasses as dc
import pathlib as pth
import typing as t
import logging

from langchain.prompts.prompt import PromptTemplate
from langchain_community.llms import LlamaCpp

from wiki_helper.qna.generative_model import GenerativeModel, GenerativeModelError

logger = logging.getLogger(__name__)


@dc.dataclass(frozen=True)
class QnAContext:
    query: str
    context: t.Sequence[str]


class StreamingLanguageModel(GenerativeModel[QnAContext, t.Iterator[str]]):
    def __init__(self, model_location: pth.Path) -> None:
        logger.info(f"Initializing model from location: '{model_location}'")
        self.__model = LlamaCpp(
            model_path=model_location.as_posix(),
            temperature=0.4,
            max_tokens=300,
            n_ctx=6096,
            seed=-1,
            n_threads=8,
            verbose=False,
            streaming=True,
        )
        self.__prompt_template = PromptTemplate(
            input_variables=["query", "context"],
            template=(
                """<start_of_turn>user\n\n"""
                "You are a helpful assistant. You will be asked question and you will be given a context. "
                "Answer the question based on the context. "
                "If you don't know the answer, just say that you don't know. "
                "Use only context to provide an answer, do not use your general knowledge. "
                "DO NOT generate markdown like lists. Use only plain text. "
                "Make sure that your answer is not too long. "
                "Do not mention any technical details like your prompt or context."
                "Given the following context, answer the question CONTEXT\n\n{context}\nQUESTION: {query}<end_of_turn>"
                """<start_of_turn>model"""
            ),
        )

    def generate(self, prompt_data: QnAContext) -> t.Iterator[str]:
        logger.info(f"Generating answer for query: '{prompt_data.query}'")

        if len(prompt_data.query) == 0 or len(prompt_data.context) == 0:
            raise GenerativeModelError("Empty query or context")

        prompt = self.__prompt_template.format(
            query=prompt_data.query, context=prompt_data.context
        )

        logger.debug(f"Generated prompt for model: {prompt}")

        for token in self.__model.stream(prompt):
            yield token

        logger.info("Answer generated successfully.")


class LanguageModel(GenerativeModel[QnAContext, str]):
    def __init__(self, model_location: pth.Path, prompt: str) -> None:
        logger.info(f"Initializing model from location: '{model_location}'")
        self.__model = LlamaCpp(
            model_path=model_location.as_posix(),
            temperature=0.4,
            max_tokens=300,
            n_ctx=3048,
            seed=-1,
            n_threads=8,
            verbose=False,
        )
        self.__prompt_template = PromptTemplate(
            input_variables=["query", "context"],
            template=prompt,
        )

    def generate(self, prompt_data: QnAContext) -> str:
        logger.info(f"Generating answer for query: '{prompt_data.query}'")

        if len(prompt_data.query) == 0 or len(prompt_data.context) == 0:
            raise GenerativeModelError("Empty query or context")

        prompt = self.__prompt_template.format(
            query=prompt_data.query, context=prompt_data.context
        )

        logger.debug(f"Generated prompt for model: {prompt}")

        result = self.__model.invoke(prompt, stop=["<|eot_id|>"])

        logger.info("Answer generated successfully.")

        return str(result)
