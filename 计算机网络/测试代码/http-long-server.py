from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_post():
    data = request.get_json()
    
    response_data = {'message': 'Received POST data', 'data': data}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=8080, debug=True, threaded=True)
