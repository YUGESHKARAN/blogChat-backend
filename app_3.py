import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Apply CORS to the app (allow all origins by default)
CORS(app)

# Define the Groq API endpoint and the API key
groq_endpoint = "https://api.groq.com/openai/v1/chat/completions"
groq_api_key = os.getenv('GROQ_API_KEY')  # Replace with your actual Groq API key

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)  
# Function to query Groq API
def query_groq_api(query):
   

    # Send the query to Groq's API and get the response
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "user", "content": query}
            ]
            )
        # Extract the generated content from the response
        generated_content = completion.choices[0].message.content
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
        # title = data.get("title")
        description = data.get("description")
        # category = data.get("category")

        # prompt = f"""
        # correct the blog content: {description}. Ensure the word limit does not exceed 150 words and generate suitable title. Avoid using subheadings or including any notes in the response.
        # """

        prompt = f"""
        You are  social media content creator. responsible for transforming given scripts into professional social media contents similar like LinkedIn post alomg with professional emojies and with tags.
        Note: 
        1. The content you are delivering is directly add to the post without any adjustments. make sure to always genrate as a final response without any options.
        2. The response format should be Markdown language.
        3. If necessary produce the content in bullet points.
        script: {description}

        """

        # Query the Groq API with the generated prompt
        generated_content = query_groq_api(prompt)

         # Remove the title from the generated content (assuming title is in the first line)
        # content_without_title = "\n".join(generated_content.splitlines()[1:])

        # Return the generated content to the frontend
        return jsonify({"content": generated_content}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
