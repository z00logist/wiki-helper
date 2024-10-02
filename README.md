# Wiki Helper
    Wiki Helper is a RAG powered QnA service. It is aimed to run locally on one's machine: either in the form of FastApi sevice or in the form of library in Jupyter Notebook.

## The Concept

Current Concept of the project is simple: 
1. You choose the topic of your interest, find the corresponding URL on Wikipedia and send it to service. Thus, you get the traineed model.
2. Optionally, you can add another article to your knowledge base, if you want to widen the system.
3. If you want to train new one, you need to delete previeous.
**Note**: Beware, that the service currently supports only one existent QnA agent at the time.

# Usage
## Locally
### Run Service

1. Install environment ```poetry install --no-root```
1.1. You may need to add src into PYTHONPATH ```export PYTHONPATH=src```
2. Run chromadb ```docker compose up -d```
3. Run service ```python -m wiki_helper```

### Use Service
#### Train Method
You need to request api methods training/train and provide it with the json containing url of wikipedia article.

#### Answer Method
Now, you trained your model and can ask it questions. You need to request api methods inference/answer and provide it with the json containing question.
