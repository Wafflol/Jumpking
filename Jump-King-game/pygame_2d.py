import json

from flask import jsonify, request
from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    # Process the data received from the client
    data = request.get_json()
    # Do something with the data
    print("asdfjlasdf")
    return "Data received and processed"


# @app.route('/testx', methods=['POST'])
# def testx():
#     data = request.get_json()
#     print(data + 2)
#     return jsonify(data)
    # output = request.get_json()
    # print(output) # This is the output that was stored in the JSON within the browser
    # print(type(output))
    # result = json.loads(output) #this converts the json output to a python dictionary
    # print(result) # Printing the new dictionary
    # print(type(result))#this shows the json converted as a python dictionary
    # return result

# @app.route('/testy', methods=['POST'])
# def testy():
#     output = request.get_json()
#     print(output) # This is the output that was stored in the JSON within the browser
#     print(type(output))
#     result = json.loads(output) #this converts the json output to a python dictionary
#     print(result) # Printing the new dictionary
#     print(type(result))#this shows the json converted as a python dictionary
#     return result
if __name__ == '__main__':
    app.run(debug=True)