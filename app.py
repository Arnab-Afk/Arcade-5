from flask import Flask, request, jsonify
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import StrOutputParser
from langchain.schema.prompt_template import format_document
from flask_cors import CORS
import os   
app = Flask(__name__)
CORS(app) 
os.environ["GOOGLE_API_KEY"] = "AIzaSyAPTMyEWrmeaUU-OgxO08fShS1YhFObFkY"

from langchain_google_genai import ChatGoogleGenerativeAI
@app.route('/api', methods=['POST'])
def generate_summary():
    data = request.get_json()
    site = data['site']
    loader = WebBaseLoader(site)
    docs = loader.load()
    