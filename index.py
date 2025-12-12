from flask import Flask, request, jsonify
from flask_cors import CORS

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langsmith import Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Client()
CORS(app)

chat_message = []
template = """
       You are  social media content creator. responsible for transforming given scripts into professional social media contents similar like LinkedIn post along with professional emojies and with tags.
       make sure to check the chat history for context before generating new content.
       Chat Message History:
       {chat_history}
        Note: 
        1. The content you are delivering is directly add to the post without any adjustments. make sure to always genrate as a final response without any options.
        2. The response format should be Markdown language.
        3. If necessary produce the content in bullet points.
        script: {description}
       
        
        
"""

model = ChatGroq(model="llama-3.1-8b-instant")

prompt = ChatPromptTemplate.from_template(template)


@app.route("/")
def welcome():
    return jsonify({"message":"welcome to chat backend content manipulator"})

@app.route("/generate-content", methods=['POST'])
def generate_content():
    try:
        data = request.json
        description = data.get("description","")

        query = prompt.invoke({"description":description, "chat_history":chat_message})

        chat_message.append({"user":query.messages[0].content})
        chain = prompt | model | StrOutputParser()
        result = chain.invoke({"description":description, "chat_history":chat_message}) 
        chat_message.append({"assistant":result})

        # print("chat history:", chat_message)

        return jsonify({"content":result}),200
    except Exception as e:
        return jsonify({"error":str(e)}), 500


if __name__ =="__main__":
    app.run(host="0.0.0.0", debug=True)

