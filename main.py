from flask import Flask, render_template, request, jsonify
from backend.chatbot_backend import load_knowledge_base, save_knowledge_base, search_response
import os


app = Flask(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
knowled_base_json_path = os.path.join(current_dir, 'json/knowledge_base.json')
knowledgeBase = load_knowledge_base(knowled_base_json_path)

# Pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/leave')
def leave():
    return render_template('leave.html')

# End Pages



# Get info

@app.route('/chatbot/messages', methods=['POST'])
def getMessages():
    data = request.get_json()
    messageType = data["messageType"]
    return jsonify({ 'message': knowledgeBase[messageType] })


# POST events 
@app.route('/get-response', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    response, exit = search_response(message, knowledgeBase)

    return jsonify({ 'response': response, 'exit': exit , 'learn': response == knowledgeBase['response_not_found']})


# Put Events
@app.route('/set-new-response', methods=['PUT'])
def setNewResponse():
    data = request.get_json()
    question = data['question']
    answer = data['answer']
    isStored = False

    try:
        knowledgeBase["question"].append({"question": question, "answer": answer})
        save_knowledge_base(knowled_base_json_path, knowledgeBase)
        isStored = True
    except:
        isStored = False


    return jsonify({ 'isStored': isStored, 'question': question , 'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)