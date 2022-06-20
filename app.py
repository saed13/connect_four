from flask import Flask, jsonify, render_template, request
from user_interface.GameBoard import GameBoard
import os

app = Flask(__name__)
JAVASCRIPT_FOLDER = os.path.join('static', 'javascript')

app.config['JAVASCRIPT_FOLDER'] = JAVASCRIPT_FOLDER
app.config['sessions'] = 0

@app.route('/')
def start_app():
    javascript = os.path.join(app.config['JAVASCRIPT_FOLDER'])
    return render_template("main.html", javascript=javascript)

@app.route('/start_game', methods=['POST'])
def start_game():
    if request.get_json()['existing_session'] == -1:
        session = app.config['sessions']

        app.config['sessions'] += 1
        if request.get_json()['mode'] == 1:
            app.config['gameBoard' + str(app.config['sessions'])] = GameBoard()
            jsonify({"session": session, "mode": 1})

        elif request.get_json()['mode'] == 2:
            app.config['gameBoard' + str(request.get_json()['existing_session'])] = GameBoard(2)
            jsonify({"session": session, "mode": 2})

        elif request.get_json()['mode'] == 3:
            app.config['gameBoard' + str(request.get_json()['existing_session'])] = GameBoard(3)
            jsonify({"session": session, "mode": 3})

    else:
        pass
        #load and render existing session
        #app.config['gameBoard' + str(request.get_json()['existing_session'])] = GameBoard()
    pass

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
