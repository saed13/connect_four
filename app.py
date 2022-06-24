from flask import Flask, jsonify, render_template, request
from user_interface.GameBoard import GameBoard
import shelve

import os

app = Flask(__name__)

JAVASCRIPT_FOLDER = os.path.join('static', 'javascript')

app.config['JAVASCRIPT_FOLDER'] = JAVASCRIPT_FOLDER

directoryName = os.path.dirname('sessions.db')
pathToSessionsDir = os.path.abspath(directoryName)


@app.route('/')
def start_app():
    file = shelve.open(f"{pathToSessionsDir}/sessions")
    try:
        sessions = file['sessions']
        file.close()
    except Exception:
        file['sessions'] = 0

    javascript = os.path.join(app.config['JAVASCRIPT_FOLDER'])
    file.close()
    return render_template("main.html", javascript=javascript)


@app.route('/start_game', methods=['POST'])
def start_game():
    file = shelve.open(f"{pathToSessionsDir}/sessions")
    if request.get_json()['existing_session'] == -1:

        session = file['sessions']
        file['sessions'] = int(session) + 1

        if request.get_json()['mode'] == 1:
            app.config['gameBoard' + str(session)] = GameBoard(1)
            file[f"session{str(session)}"] = app.config['gameBoard' + str(session)]
            file.close()
            return jsonify({"session": session, "mode": 1})

        elif request.get_json()['mode'] == 2:
            app.config['gameBoard' + str(session)] = GameBoard(2)
            file[f"session{str(session)}"] = app.config['gameBoard' + str(session)]
            file.close()
            return jsonify({"session": session, "mode": 2})

        elif request.get_json()['mode'] == 3:
            app.config['gameBoard' + str(session)] = GameBoard(3)
            file[f"session{str(session)}"] = app.config['gameBoard' + str(session)]
            file.close()
            return jsonify({"session": session, "mode": 3})

    else:
        pass
        # load and render existing session
        # app.config['gameBoard' + str(request.get_json()['existing_session'])] = GameBoard()
    pass


@app.route('/post_pos', methods=['POST'])
def get_pos():
    file = shelve.open(f"{pathToSessionsDir}/sessions")
    if not request.get_json()['AIMove']:
        col = app.config['gameBoard' + str(request.get_json()['session'])].get_input(request.get_json()['x'])
        if col != -1:
            row = app.config['gameBoard' + str(request.get_json()['session'])].add_token(col)
            file[f"session{str(request.get_json()['session'])}"] = row[4]

            file.close()
            return jsonify({'full': False, 'winner': row[0], 'pos': row[1], 'p1': row[2], 'finished': row[3]}), 200
        file.close()
        return jsonify({'full': True}), 200

    elif request.get_json()['AIMove']:
        row = app.config['gameBoard' + str(request.get_json()['session'])].AI_move()
        file[f"session{str(request.get_json()['session'])}"] = row[4]

        file.close()
        if row == "full":
            return jsonify({'full': True}), 200
        return jsonify({'full': False, 'winner': row[0], 'pos': row[1], 'p1': row[2], 'finished': row[3]}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0")
