# Web Page Summary Generator

## Overview

This project is a Flask-based web application that generates concise summaries of web pages using Google's Generative AI (Gemini). The application leverages LangChain to load web pages and format the content, then uses Google's AI to generate the summaries.

## Features

- **Flask Backend:** A web server to handle API requests.
- **LangChain Integration:** To load and format web page content.
- **Google Generative AI:** To generate concise summaries of the web page content.
- **CORS:** To allow cross-origin requests.

## Setup and Installation

### Prerequisites

- Python 3.7+
- Flask
- LangChain
- LangChain Community
- Flask-CORS

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-repo/web-page-summary-generator.git
    cd web-page-summary-generator
    ```

2. **Create a virtual environment:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**

    ```sh
    pip install flask flask-cors langchain langchain_community
    ```

4. **Set up your environment variables:**

    Add your Google API key to the environment:

    ```sh
    export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    ```

## Project Structure

```plaintext
web-page-summary-generator/
│
├── app.py                # Main application file
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
└── venv/                 # Virtual environment
```

## Application Code
Below is a detailed explanation of the main application code in app.py.

```python 
from flask import Flask, request, jsonify
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import StrOutputParser
from langchain.schema.prompt_template import format_document
from flask_cors import CORS
import os   
```

## Initialize Flask and CORS

```python 
app = Flask(__name__)
CORS(app) 
os.environ["GOOGLE_API_KEY"] = "API-KEY"
```

## Import Google Generative AI
```python 
from langchain_google_genai import ChatGoogleGenerativeAI
```

## Define API Endpoint
This endpoint accepts a POST request with a JSON body containing the URL of the site to be summarized.
```python 
@app.route('/api', methods=['POST'])
def generate_summary():
    data = request.get_json()
    site = data['site']
    loader = WebBaseLoader(site)
    docs = loader.load()
    
    doc_prompt = PromptTemplate.from_template("{page_content}")
    llm_prompt_template = """Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:"""
    llm_prompt = PromptTemplate.from_template(llm_prompt_template)
    
    llm = ChatGoogleGenerativeAI(model="gemini-pro",
                                 temperature=0.7, top_p=0.85)
    
    stuff_chain = (
        {
            "text": lambda docs: "\n\n".join(
                format_document(doc, doc_prompt) for doc in docs
            )
        }
        | llm_prompt         # Prompt for Gemini
        | llm                # Gemini function
        | StrOutputParser()  # output parser
    )
    
    response = stuff_chain.invoke(docs)
    
    return jsonify({"summary": response})
```

## Run the Application
```python if __name__ == '__main__':
    app.run(debug=True)
```

# How to Use
## Starting the Server
To start the Flask server, run:
```bash 
python app.py
```


## Making a Request
Send a POST request to http://localhost:5000/api with a JSON body containing the site URL you want to summarize. Example:
```bash 
curl -X POST http://localhost:5000/api \
    -H "Content-Type: application/json" \
    -d '{"site": "https://example.com"}'
```


## Response
The server will respond with a JSON object containing the summary:
```json 
{
    "summary": "Concise summary of the web page content."
}
```
## Notes
- Ensure that you have set the GOOGLE_API_KEY environment variable correctly.
- Adjust the model parameters (temperature, top_p) in the ChatGoogleGenerativeAI instantiation to fine-tune the summaries.


## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

