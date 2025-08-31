import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
from dotenv import load_dotenv
# from openai import OpenAI
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from langsmith import  Client
# Load environment variables from .env file
load_dotenv()

client = Client()

# Initialize the Flask application
app = Flask(__name__)

# Apply CORS to the app (allow all origins by default)
CORS(app)


genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# # Function to query Gemini API
# @traceable(name="blogbrowser-backend")
def query_gemini(query):
    try:
        response = model.generate_content(query)
        return response.text
    except GoogleAPIError as e:
        return f"Error querying Gemini API: {str(e)}"
@app.route("/") 
def index():
    return "Welcome to the Blog Content Generator API!"

@app.route("/generate-content", methods=["POST"])
def generate_blog_content():
    try:
        # Get user input from the frontend
        data = request.json
        # title = data.get("title")
        description = data.get("description")
        # category = data.get("category")

      
        
        prompt = f"""
        You are  social media content creator. responsible for transforming given scripts into professional social media contents similar like LinkedIn post alomg with professional emojies and with tags.
        Note: 
        1. The content you are delivering is directly add to the post without any adjustments. make sure to always genrate as a final response without any options.
        2. The response format should be Markdown language.
        3. If necessary produce the content in bullet points.
        script: {description}

        """

        # Query the Groq API with the generated prompt
        generated_content = query_gemini(prompt)

         # Remove the title from the generated content (assuming title is in the first line)
        # content_without_title = "\n".join(generated_content.splitlines()[1:])

        # Return the generated content to the frontend
        return jsonify({"content": generated_content}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
