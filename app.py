import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
from dotenv import load_dotenv  

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Apply CORS to the app (allow all origins by default)
CORS(app)

# Define the Groq API endpoint and the API key
groq_endpoint = "https://api.groq.com/openai/v1/chat/completions"
groq_api_key = os.getenv('GROQ_API_KEY')  # Replace with your actual Groq API key

# Function to query Groq API
def query_groq_api(query):
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",  # Replace with your desired model
        "messages": [
            {"role": "user", "content": query}
        ]
    }

    # Send the query to Groq's API and get the response
    try:
        response = requests.post(groq_endpoint, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error if the request failed
        data = response.json()
        # Extract the generated content from the response
        generated_content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return generated_content
    except requests.exceptions.RequestException as e:
        return f"Error querying Groq API: {str(e)}"
    
@app.route("/") 
def index():
    return "Welcome to the Blog Content Generator API!"

@app.route("/generate-content", methods=["POST"])
def generate_blog_content():
    try:
        # Get user input from the frontend
        data = request.json
        title = data.get("title")
        description = data.get("description")
        category = data.get("category")

        # Create a prompt template based on user input
        prompt = f"Create a blog post about '{title}'. The blog should focus on {description} under the category of {category}. Provide a catchy introduction, subheadings, and a conclusion. note: word limit strictly 80 words."

        # Query the Groq API with the generated prompt
        generated_content = query_groq_api(prompt)

         # Remove the title from the generated content (assuming title is in the first line)
        content_without_title = "\n".join(generated_content.splitlines()[1:])

        # Return the generated content to the frontend
        return jsonify({"content": content_without_title}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
