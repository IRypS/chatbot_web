from flask import Flask, render_template, request, jsonify
from backend.chatbot_backend import load_knowledge_base, save_knowledge_base, search_response

app = Flask(__name__)

knowled_base_json_path = 'json/knowledge_base.json'
knowledgeBase = load_knowledge_base(knowled_base_json_path)

# Pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

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


    # TODO: EXIT
    # TODO: LEARN

    return jsonify({ 'response': response })

if __name__ == '__main__':
    app.run(debug=True)