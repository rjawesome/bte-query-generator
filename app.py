from tester import question_to_json
from flask import Flask, Response, render_template, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/api', methods=['GET'])
def handle_question():
    question = request.args.get('question')
    output = question_to_json(question)
    if output.startswith('{'):
        return Response(output, mimetype='application/json')
    return output

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=10101)
