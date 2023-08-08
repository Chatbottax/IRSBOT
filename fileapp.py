from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

# Load the OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# Name of the chatbot
chatbot_name = "Tax Resolution Assistant"

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']
    user_name = data.get('name', 'User')  # Get the user's name if provided, else default to 'User'

    # Initial system message
    system_message = f'You are {chatbot_name}, an AI developed by OpenAI, functioning as a Tax Resolution Expert. You provide guidance on the IRS Fresh Start Program. Once you have the necessary information, you will inform the client that our Case Manager, Sami, will be calling them shortly. Sami can be reached directly at Sami@freshstarttaxco.com or 858-649-9433 during office hours (9 AM to 5 PM EST, Monday through Friday).'

    # Process the user message with OpenAI
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': user_message},
        ]
    )

    response_dict = dict(response)
    chatbot_message = response_dict['choices'][0]['message']['content']

    # Personalization
    chatbot_message = chatbot_message.replace('User', user_name)

    # Guided prompts
    if 'penalties' in user_message.lower():
        chatbot_message += ' Would you like to know more about how to reduce these penalties?'

    return jsonify({'message': chatbot_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
