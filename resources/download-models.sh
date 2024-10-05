huggingface-cli download mixedbread-ai/mxbai-embed-large-v1 --local-dir ./models/embedder/ --include "*.safetensors" --include "*.json" --include "*.txt"

huggingface-cli download  unsloth/Llama-3.2-3B-Instruct-GGUF --include "Llama-3.2-3B-Instruct-Q6_K.gguf" --local-dir ./models/generative_model/