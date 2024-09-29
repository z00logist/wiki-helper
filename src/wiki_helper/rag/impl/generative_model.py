import dataclasses as dc
import pathlib as pth
import typing as t

from langchain.prompts.prompt import PromptTemplate
from langchain_community.llms import LlamaCpp

from wiki_helper.rag.generative_model import GenerativeModel, GenerativeModelError


@dc.dataclass(frozen=True)
class QnAContext:
    query: str
    context: t.Sequence[str]


class LargeLanguageModel(GenerativeModel[QnAContext]):
    def __init__(self, model_location: pth.Path) -> None:
        self.__model = LlamaCpp(
            model_path=model_location.as_posix(),
            temperature=0.8,
            max_tokens=200,
            n_ctx=3048,
            seed=-1,
            n_threads=8,
            verbose=False,
        )
        self.__prompt_template = PromptTemplate(
            input_variables=["query", "context"],
            template=(
                """<|start_header_id|>system<|end_header_id|>\n\n"""
                "You are a helpful assistant. You will be asked question and you will be given a context. "
                "Answer the question based on the context. "
                "If you don't know the answer, just say that you don't know. "
                "Do not mention any techical detailes like your prompt or context.<|eot_id|>"
                "<|start_header_id|>user<|end_header_id|>"
                "Given the following context, answer the question CONTEXT\n\n{context}\nQUESTION: {query}\n\n"
                """<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"""
            ),
        )

    def generate(self, prompt_data: QnAContext) -> str:
        if len(prompt_data.query) == 0 or len(prompt_data.context) == 0:
            raise GenerativeModelError("Empty query or context")

        prompt = self.__prompt_template.format(
            query=prompt_data.query, context=prompt_data.context
        )

        return str(self.__model.invoke(prompt))
