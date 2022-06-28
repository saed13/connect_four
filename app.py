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
    print(pathToSessionsDir)
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
        print(list(file.keys()))

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


@app.route('/savegame', methods=['POST'])
def get_savegame():
    file = shelve.open(f"{pathToSessionsDir}/sessions")

    session = file[str(request.get_json()['session'])]

    print(session.board)
    saves = jsonify({"board": session.board, "mode": session.mode})

    return saves


@app.route('/saves', methods=['POST'])
def get_saves():
    file = shelve.open(f"{pathToSessionsDir}/sessions")
    sessions = file["sessions"]
    print(f"sessions {sessions}")
    session = [None, None, None]
    r = int(sessions)
    counter = 0
    for i in range(r - 1, -1, -1):
        print(list(file.keys()))
        print(i)
        s = file[f"session{str(i)}"]
        print(s.winner)

        if s.winner == None:
            print(counter)
            session[counter] = f"session{str(i)}"
            counter += 1
        if counter >= 3:
            break

    saves = jsonify({"s1": session[0], "s2": session[1], "s3": session[2]})

    return saves


def check_save(s):
    pass


@app.route('/post_pos', methods=['POST'])
def get_pos():
    file = shelve.open(f"{pathToSessionsDir}/sessions")
    if not request.get_json()['AIMove']:
        col = file['session' + str(request.get_json()['session'])].get_input(request.get_json()['x'])
        if col != -1:
            row = file['session' + str(request.get_json()['session'])].add_token(col)
            file[f"session{str(request.get_json()['session'])}"] = row[4]

            file.close()
            return jsonify({'full': False, 'winner': row[0], 'pos': row[1], 'p1': row[2], 'finished': row[3]}), 200
        file.close()
        return jsonify({'full': True}), 200

    elif request.get_json()['AIMove']:
        row = file['session' + str(request.get_json()['session'])].AI_move()
        file[f"session{str(request.get_json()['session'])}"] = row[4]

        file.close()
        if row == "full":
            return jsonify({'full': True}), 200
        return jsonify({'full': False, 'winner': row[0], 'pos': row[1], 'p1': row[2], 'finished': row[3]}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
