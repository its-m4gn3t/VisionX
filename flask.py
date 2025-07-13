from flask import Flask, request, jsonify, render_template_string
import ollama

app = Flask(__name__)

# Simple HTML page for user input
HTML = 
<html>
<body>
  <h2>Ollama Chat</h2>
  <form method="post" action="/chat">
    <input type="text" name="prompt" placeholder="Enter your prompt" size="50"/>
    <input type="submit" value="Send"/>
  </form>
  {% if response %}
    <p><strong>Response:</strong> {{ response }}</p>
  {% endif %}
</body>
</html>


@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.form.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    # Call Ollama generate API
    result = ollama.generate(model='llama2', prompt=prompt)
    response = result.get('response', 'No response')
    return render_template_string(HTML, response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
