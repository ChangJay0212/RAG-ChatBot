# Chatbot Service

This chatbot provides RAG (Retrieval-Augmented Generation) functionality, allowing users to easily ask questions. The model used for this service is based on [Ollama](https://github.com/ollama/ollama). The frontend is implemented using [Streamlit](https://github.com/streamlit/streamlit).

## User Usage
![image](/docs/example.gif)

### Start the Service

To start the Chatbot service, use Docker Compose with the provided configuration file:

```bash
docker compose -f ./compose.yaml up -d
# Enter bash 
docker exec -it rag_v1 /bin/bash

# Operate With WebUI : http://127.0.0.1:8000/static/index.html
# Open API docs : http://127.0.0.1:8000/docs
# Open traces : http://127.0.0.1:6006 
```

### Shutdown service
```bash
docker compose down
```

### How to update vector database?
* Follow [Vectorization](/docs/Vectorization.md) to update new data to vector database.

## Other
* [Development readme](/docs/README.DEV.md) 
* [Update map](/docs/UPDATE.md)
* [Todo](/docs/TODO.md)

