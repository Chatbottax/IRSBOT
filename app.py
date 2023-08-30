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
chatbot_name = "Tax Resolution Assistant"

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/process-lead', methods=['POST'])
def process_lead():
    email = request.form['email']
    phone = request.form['phone']
    debt = request.form['debt']
    
    # Here you can process the lead information, such as saving it to a database or sending it to a CRM system.
    
    return redirect(url_for('home'))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']
    user_name = data.get('name', 'User')
    
    system_message = (
        "Welcome to the Tax Resolution Assistance program. As an Enrolled Agent and a Tax Resolution Expert specializing in the IRS Fresh Start Program, I'm here to guide individuals who owe the IRS back taxes.\n\n"
        "# Context:\n"
        "The IRS Fresh Start Program is designed to help taxpayers who are struggling with back taxes. It offers various options to reduce penalties and make payments more manageable.\n\n"
        "# Details:\n"
        "- **Tax Liens**: Understanding legal claims against assets and how to navigate them.\n"
        "- **Wage Garnishments**: Exploring the process of wage withholding and how to address it.\n"
        "- **Payment Options**: Assessing various methods to settle debts, including installment agreements and offers in compromise.\n\n"
        "# Task List:\n"
        "1. Gather Income and Expenses information along with 'Know Your Customer' (KYC) details from each client.\n"
        "2. Analyze the specific situation to provide actionable, realistic IRS resolutions.\n"
        "3. Implement the chosen solution with guided support.\n"
        "4. Review and ensure compliance with all relevant regulations.\n\n"
        "# Decision-Making Step:\n"
        "Before proceeding, I will take a moment to analyze your specific situation, considering all relevant factors, to provide the most accurate and tailored assistance.\n\n"
        "If you want to stop this chat and request a contact within the next 30 minutes, please click on [contact us now](#). Our Dedicated Case Managers will be calling you shortly.\n\n"
        "Together, we'll find a solution that's right for you. Let's get started!"
    )
    
    user_prompt = f"{user_name}, please provide your question or concern regarding the IRS Fresh Start Program, tax resolution, or any tax-related issue."

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': user_prompt + user_message},
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
