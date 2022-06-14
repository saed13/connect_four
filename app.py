from flask import Flask, jsonify, render_template, request
from user_interface.GameBoard import GameBoard
import os

app = Flask(__name__)
JAVASCRIPT_FOLDER = os.path.join('static', 'javascript')

app.config['JAVASCRIPT_FOLDER'] = JAVASCRIPT_FOLDER
app.config['sessions'] = 0

@app.route('/')
def start_app():
    app.config['gameBoard' + str(app.config['sessions'])] = GameBoard()

    javascript = os.path.join(app.config['JAVASCRIPT_FOLDER'])
    app.config['sessions'] += 1

    return render_template("main.html", javascript=javascript, session=app.config['sessions'] - 1, mode=2)


@app.route('/post_pos', methods=['POST'])
def get_pos():
    if not request.get_json()['AIMove']:
        col = app.config['gameBoard' + str(request.get_json()['session'])].get_input(request.get_json()['x'])
        if col != -1:
            row = app.config['gameBoard' + str(request.get_json()['session'])].add_token(col)
            return jsonify({'full': False, 'winner': row[0], 'pos': row[1], 'p1': row[2], 'finished': row[3]}), 200

        return jsonify({'full': True}), 200

    elif request.get_json()['AIMove']:
        row = app.config['gameBoard' + str(request.get_json()['session'])].AI_move()
        if row == "full":
            return jsonify({'full': True}), 200
        return jsonify({'full': False, 'winner': row[0], 'pos': row[1], 'p1': row[2], 'finished': row[3]}), 200


if __name__ == '__main__':
    app.run()
