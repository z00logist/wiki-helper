# Wiki Helper
Wiki Helper is a RAG-powered QnA service. It is aimed to run locally on one's machine: either in the form of FastApi sevice or in the form of library in Jupyter Notebook.

## The Concept

Current Concept of the project is simple: 
1. You choose the topic of your interest, find the corresponding URL on Wikipedia and send it to service. Thus, you get the traineed model.
2. Optionally, you can add another article to your knowledge base, if you want to widen the system.
3. If you want to train a new one, you need to delete previous.
**Note**: Beware, that the service currently supports only one QnA agent **in English** at the time. 

# Usage
## Locally
### Preparation

1. Install environment ```poetry install --no-root```  
2. Download baseline models: ```sh /resources/download-models.sh```

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

## Via Jupter Notebook
### Preparation

1. Install environment ```poetry install --no-root```  
2. Download baseline models: ```/resources/download-models.sh```

### Use Notebook
You can find the example of usage in [examples/](examples)