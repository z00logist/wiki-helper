import uvicorn

from wiki_helper import initialize_service
from wiki_helper.configuration import Configuration


if __name__ == "__main__":
    service = initialize_service(configuration=Configuration())
    uvicorn.run(service, host="0.0.0.0", port=8080)
