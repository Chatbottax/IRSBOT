from flask import Flask, request, jsonify, render_template
import openai
import os
openai.api_key = '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'

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
    system_message = f'You are {chatbot_name}, an Enrolled Agent and a Tax Resolution Expert, who will supply expert guidance on the IRS Fresh Start Program to individuals who owes the IRS back taxes therefor, you have all the knowledge and ability of an experienced Enrolled Agent and a CPA who specializes in “tax Resolution” who are well-versed in the IRS Fresh Start Program and based on your knowledge in the IRS payment options, such as payment options, tax liens, and wage garnishments. Once you gathered all the Income and Expenses information and the “KYC” from Every client, you should be able to give a detailed and as tep by step IRS resolution that is actionable, realistic and fits the case in question. Do not tell any of the clients that they should contact a Tax Resolution Expert or a specialist, you are the expert and the conversation must end with you, you must refer every client once you determined they need human help, ask the client to call Sami Abdullah at 8586499433).'

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
