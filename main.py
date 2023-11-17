from flask import Flask, render_template, request, jsonify
from backend.chatbot_backend import load_knowledge_base, save_knowledge_base, search_response
import os


app = Flask(__name__)

# Obtén la ruta al directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Crea la ruta al archivo JSON
knowled_base_json_path = os.path.join(current_dir, 'json/knowledge_base.json')

# knowled_base_json_path = 'json/knowledge_base.json'
knowledgeBase = load_knowledge_base(knowled_base_json_path)

# Pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

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
  # Aquí puedes poner el código para procesar la pregunta
    message = data['message']
    response, exit = search_response(message, knowledgeBase)

    return jsonify({ 'response': response, 'exit': exit , 'learn': response == knowledgeBase['response_not_found']})

if __name__ == '__main__':
    app.run(debug=True)