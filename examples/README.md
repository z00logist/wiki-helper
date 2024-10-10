# Wiki Helper (Developer Guide)
Wiki Helper is a RAG-powered Q&A service that runs locally, either as a FastAPI service or as a library in Jupyter Notebook. It processes Wikipedia articles and allows users to interact with a Q&A model trained on those articles.

## The Concept

The current concept is simple:
1. You choose a topic of interest, find the corresponding Wikipedia URL, and send it to the service. This trains the model on that article.
2. You can optionally add more articles to your knowledge base.
3. To train a new model, you need to delete the previous one.

**Note:** The service currently supports only one QnA agent **in English** at a time.

## Usage
### Locally

#### Preparation
### Preparation

1. Install environment ```poetry install --no-root```  
2. Download baseline models: ```resources/download-models.sh```

### Run the Service
0. You may need to add src into PYTHONPATH ```export PYTHONPATH=src```
2. Run chromadb ```docker compose up -d```
3. Run service ```python -m wiki_helper```

### Use Service
#### Train
You need to request api methods training/train and provide it with the json containing url of wikipedia article.
Request parameters:
**URL**   

For example: 
```curl -X POST "http://0.0.0.0:8080/training/train" -H "Content-Type: application/json" -d "{\"url\": \"https://en.wikipedia.org/wiki/Programming_language\"}"```
#### Answer
Now, you trained your model and can ask it questions. You need to request api methods inference/answer and provide it with the json containing question.
Request parameters:
**Question**   

For example: 
```curl -X POST "http://0.0.0.0:8080/inference/answer" -H "Content-Type: application/json" -d "{\"question\": \"What is Python?\"}"```

## Via Jupyter Notebook
### Preparation

1. Install environment ```poetry install --no-root```  
2. Download baseline models: ```resources/download-models.sh```

### Use Notebook
You can find the example of usage in [examples/](examples)