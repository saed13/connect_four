let finished = false,
    newGameBtn = document.getElementById("newGame"),
    joinGameBtn = document.getElementById("joinGame"),
    board = document.querySelector(".board"),
    startMenu = document.querySelector("#startMenu"),
    AI = false,
    sessionNum = null,
    mode = null,
    PvP = null,
    AIvAI = null,
    PvAI = null;

//createBoard()

newGameBtn.addEventListener('click',  newGame);


function messageWindow(winner){

    let modal = document.createElement("div");
    //modal.setAttribute("modal",winner + "wins!");
    modal.classList.add("modal");

    let modal_content = document.createElement("div");
    modal_content.classList.add("modal-content")
    if (winner === "P1") {
        modal_content.style.backgroundColor = "#D81159";
    } else if(winner === "P2") {
        modal_content.style.backgroundColor = "#FFBC42";
    }

    modal.appendChild(modal_content)

    let span = document.createElement("span");
    span.classList.add("close");
    modal.setAttribute("span","&times;");

    modal_content.appendChild(span)

    let p = document.createElement("p");
    p.classList.add("p");
    //p.setAttribute("p",winner + "wins!");
    p.innerHTML = winner + " has won the game!"
    modal_content.appendChild(p)

    let modals = document.getElementById("modals")
    modals.appendChild(modal)
    modal.style.display = "flex";

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    /*window.onclick = function(event) {
      if (event.target === modal) {
        modal.style.display = "none";
      }
    }

     */
}

function newGame() {
    //messageWindow('p1');

    newGameBtn.hidden = true;
    joinGameBtn.hidden = true;
    let bt1 = document.createElement("button");
    PvP = bt1;
    bt1.setAttribute("bt1","PvP");
    bt1.innerHTML = "PvP";
    bt1.addEventListener('click', () => {
        chooseMode(1);
    });
    bt1.id = "pvp"
    startMenu.appendChild(bt1);

    let bt2 = document.createElement("button");
    PvAI = bt2;
    bt2.setAttribute("bt2","PvAI");
    bt2.innerHTML = "PvAI";
    bt2.addEventListener('click', () => {
        chooseMode(2);
    });
    bt2.id = "pvai"
    startMenu.appendChild(bt2);

    let bt3 = document.createElement("button");
    AIvAI = bt3;
    bt3.setAttribute("bt3","AIvAI");
    bt3.innerHTML = "AIvAI";
    bt3.addEventListener('click', () => {
        chooseMode(3);
    });
    bt3.id = "aivai"
    startMenu.appendChild(bt3);

}

function chooseMode(gameMode) {
    const body = {
        mode: gameMode,
        existing_session: -1
    }

    fetch('/start_game',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
              'Accept': 'application/json'
        },
        body: JSON.stringify(body)
    }).then((response) => response.json())
        .then(res => {
            document.getElementById('sessionNum').value = res.session;
            sessionNum = res.session;
            mode = res.mode;
            startMenu.parentNode.removeChild(startMenu);
            PvP.parentNode.removeChild(PvP);
            PvAI.parentNode.removeChild(PvAI);
            AIvAI.parentNode.removeChild(AIvAI);
            board.hidden = false;
            createBoard();
        });
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


        board.appendChild(div);

        if (x === 6) {
            y--;
        }
    }
    if (mode === 3) {
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
                            messageWindow("P1");
                        } else {
                            document.getElementById(`col${res.pos[0]}-row${res.pos[1]}`).classList.add("player-two");
                            document.getElementById("winner").value = "p2";
                            messageWindow("P2");
                        }

                        finished = true;
                    } else if (!res.finished) {

                        if (res.p1) {
                            document.getElementById(`col${res.pos[0]}-row${res.pos[1]}`).classList.add("player-one");
                            if (mode === 2 && !AI) {
                                AI = true;
                                setTimeout(() => {
                                    sendPos(null, true);
                                }, 500);
                            } else if (mode === 3) {
                                setTimeout(() => {
                                    sendPos(null, true);
                                }, 500);
                            } else if (AI) {
                                AI = false
                            }
                        } else {
                            document.getElementById(`col${res.pos[0]}-row${res.pos[1]}`).classList.add("player-two");
                            if (mode === 2 && !AI) {
                                AI = true;
                                setTimeout(() => {
                                    sendPos(null, true);
                                }, 500);
                            } else if (mode === 3) {
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
