# Vectorization Service Script

## Overview

This script is designed to process and vectorize datasets using different models based on the type of data (PDF or image). It utilizes the MinillmModel for text embeddings. The vectorized data is then used to update a vector database, stored in a specified table within a database.

## Usage

### Command-Line Arguments

| Argument               | Required | Description                                                                                 |
|------------------------|----------|---------------------------------------------------------------------------------------------|
| `-h, --help`           | No       | Show the help message and exit.                                                             |
| `-d, --data_folder`    | Yes      | The path of the dataset. Must be a valid path.                                              |
| `-t, --table_name`     | No       | The table name to save vectorization data. Default is `rag_data`.                           |
| `-tools`               | No       | The RAG method to create vectorization data. Default is `default`. Use `ai` for optimized data. |

### Running the Script

To run the script, use the following command:

```bash
python3 vectorization.py -d <data_folder> -t <table_name> -tools <tools>
```

#### For PDFs

If processing PDF files, the data folder should contain:

```bash
data_folder/
├── file1.pdf
├── file2.pdf
└── (other PDF files)
```

### Example Commands
To process a dataset with PDF files and use the default table name and method:

```bash
python3 vectorization.py -d /path/to/data_folder
```

Use ai to chunk data, vectorize a dataset and save it to a specific table:

```bash
python3 vectorization.py -d /path/to/data_folder -t custom_table -tools ai
```



