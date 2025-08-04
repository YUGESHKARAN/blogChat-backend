import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
from dotenv import load_dotenv
# from openai import OpenAI
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

from langsmith import traceable, Client
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

# Function to query Gemini API
@traceable(name="blogbrowser-backend")
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

        # prompt = f"""
        # correct the blog content: {description}. Ensure the word limit does not exceed 150 words and generate suitable title. Avoid using subheadings or including any notes in the response.
        # """

        prompt = f""""
        You are a content checker used to correct the syntax of the given context of the user.
        FOR EXAMPLE:
        Context: I have done second task my data science internship in CompWallah.
        Output: Presenting the outcome of my second task during the Data Science internship: Health Insurance Premium Prediction, assigned by CompWallah.

    
        📊 #DataScience #Internship #CompWallah #HealthInsurance #PremiumPrediction
           
        Note: 
        1. Do not mention chatbot content like eg. 'sure i can help...' response in the output. send back the corrected content only along with #terms.
        2. Make sure to add professional relevant emojis.
        3. If description is empty ask them to enter the post content to modify.
        3. Avoid adding new content
        4.Make it as humanized,  do not include AI content like -  Thrilled to announce that.
        its your turn:
        context:{description}
        Output:
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
