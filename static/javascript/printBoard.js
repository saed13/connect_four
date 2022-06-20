let finished = false,
    newGameBtn = document.getElementById("newGame"),
    board = document.querySelector(".board"),
    AI = false,
    sessionNum = null,
    mode = null;

//createBoard()

newGameBtn.addEventListener('click',  newGame);

function newGame() {

}

function existingGame() {

}
//createBoard function, creates the board
function createBoard(){
    let y = 5;
    for(let i = 0; i < 42; i++){
        let div = document.createElement("div");
        div.setAttribute("data-id", i);
        div.className = "square";

        let x = i % 7;
        div.id = `col${x}-row${y}`
        div.addEventListener('click', () => {
            AI = false;
            sendPos(x*100+6, false);
        });


        board.appendChild(div)

        if (x === 6) {
            y--;
        }
    }
    if (mode === '3') {
        setTimeout(() => {
            sendPos(Math.floor(Math.random() * 6)*100+6, false);
        }, 1000);
    }
}

//sendPos function, gets the position of the piece and sends it to the server
const sendPos = (col, AIMove) => {
    console.log("ai move: ", AIMove);

    let body = {
        x: col,
        session: sessionNum,
        AIMove: AIMove
    }

    fetch('/post_pos',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(body)
        })
            .then((response) => response.json())
            .then(res => {
                if (!res.full) {
                    if (res.finished && !finished) {
                        if (res.p1) {
                            document.getElementById(`col${res.pos[0]}-row${res.pos[1]}`).classList.add("player-one");
                            document.getElementById("winner").value = "p1";
                        } else {
                            document.getElementById(`col${res.pos[0]}-row${res.pos[1]}`).classList.add("player-two");
                            document.getElementById("winner").value = "p2";
                        }

                        finished = true;
                    } else if (!res.finished) {

                        if (res.p1) {
                            document.getElementById(`col${res.pos[0]}-row${res.pos[1]}`).classList.add("player-one");
                            if (mode === '2' && !AI) {
                                AI = true;
                                setTimeout(() => {
                                    sendPos(null, true);
                                }, 500);
                            } else if (mode === '3') {
                                setTimeout(() => {
                                    sendPos(null, true);
                                }, 500);
                            } else if (AI) {
                                AI = false
                            }
                        } else {
                            document.getElementById(`col${res.pos[0]}-row${res.pos[1]}`).classList.add("player-two");
                            if (mode === '2' && !AI) {
                                AI = true;
                                setTimeout(() => {
                                    sendPos(null, true);
                                }, 500);
                            } else if (mode === '3') {
                                setTimeout(() => {
                                    sendPos(null, true);
                                }, 500);
                            } else if (AI) {
                                AI = false;
                            }
                            //document.getElementById(`col${res.col}-row${res.pos[1]}`).style.backgroundColor = "#ffeb3b";
                        }
                    }
                }
            });
}
