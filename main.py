from flask import Flask, render_template, jsonify, request
from utils import load_champs_list, load_picked_champs, save_picked_champs

app = Flask(__name__)

champs = load_champs_list()
picked = load_picked_champs()

@app.route('/champs/picked', methods=['GET', 'POST'])
def picked_champs_list():
    if request.method == 'GET':
        return jsonify({'champs': picked}), 200
    
    if request.method == 'POST':
        data = request.json['champs']
        for champ in data:
            picked.append(champ['name'])
        
        picked = list(set(picked))
        save_picked_champs(picked)
        return jsonify({'message': 'Saved Successfully'}), 200


@app.route('/champs')
def champs_list():
    return jsonify({'champs': champs}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)