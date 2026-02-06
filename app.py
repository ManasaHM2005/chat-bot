from flask import Flask
#from ai import get_ai_response

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

#@app.route('/chat', methods=['POST'])
#def chat():
#    user_input = request.json['message']
#    ai_response = get_ai_response(user_input)
#    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)