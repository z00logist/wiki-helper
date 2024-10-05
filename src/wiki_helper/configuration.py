import pathlib as pth

from pydantic_settings import BaseSettings
from pydantic import Field


class BaseSettingsConfig(BaseSettings):
    class Config:
        env_nested_delimiter = "__"


class Storage(BaseSettingsConfig):
    host: str = "localhost"  # NOTE: no need to change as the service runs locally
    port: int = 8000


class Embedder(BaseSettingsConfig):
    location: pth.Path = Field(
        default=pth.Path.cwd() / "models" / "embedder",
        description="Path to the embedding model directory",
    )


class LLM(BaseSettingsConfig):
    location: pth.Path = Field(
        default=pth.Path.cwd()
        / "models"
        / "generative_model"
        / "Llama-3.2-3B-Instruct-Q6_K.gguf",
        description="Path to the large language model",
    )


class Configuration(BaseSettingsConfig):
    storage: Storage = Storage()
    embedder: Embedder = Embedder()
    llm: LLM = LLM()
    language: str = "en"  # NOTE:  stub for now, can be expanded in the future
