from flask import Flask, request, jsonify, render_template, redirect, url_for
import openai
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

# Name of the chatbot
chatbot_name = "Fresh Start Tax Expert"

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/process-lead', methods=['POST'])
def process_lead():
    email = request.form['email']
    phone = request.form['phone']
    debt = request.form['debt']
    
    # Process the lead information (e.g., save to a database, send to CRM)
    # [Add your code here]
    
    return redirect(url_for('home'))

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data['message']
        user_name = data.get('name', 'User')
        
        system_message = (
            "You are an expert on the IRS Fresh Start Program, "
            "specializing in tax resolution. Please provide comprehensive "
            "and actionable guidance to individuals seeking help with their tax issues. "
            "Do not refer users to external tax resolution experts; "
            "provide complete assistance within this conversation."
        )
        
        user_prompt = f"{user_name}, please share your question or concern about tax issues: "

        response = openai.ChatCompletion.create(
            model='ft:gpt-3.5-turbo-0613:personal::86xqjIn8',
            messages=[
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': user_prompt + user_message},
            ]
        )

        chatbot_message = response['choices'][0]['message']['content']
        
        # Personalization
        chatbot_message = chatbot_message.replace('User', user_name)

        return jsonify({'message': chatbot_message})
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'message': "I'm sorry, but I'm unable to respond at the moment. Please try again later."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)


