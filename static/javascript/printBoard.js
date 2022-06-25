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
joinGameBtn.addEventListener('click', getSavedGames);

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
    modal.onclick = function() {
      modal.style.display = "none";
      window.location.reload()
    }

}
function joinGame(s1,s2,s3){

    newGameBtn.hidden = true;
    joinGameBtn.hidden = true;
    let sv1 = document.createElement("button");
    sv1.innerHTML = s1;
    sv1.addEventListener('click',() => getSavedGame(s1))
    sv1.id = "sv1"
    startMenu.appendChild(sv1);
    let sv2 = document.createElement("button");
    sv2.innerHTML = s2;
    sv2.addEventListener('click',() => getSavedGame(s2))
    sv2.id = "sv2"
    startMenu.appendChild(sv2);
    let sv3 = document.createElement("button");
    sv3.innerHTML = s3;
    sv3.addEventListener('click',() => getSavedGame(s3))
    sv3.id = "sv3"
    startMenu.appendChild(sv3);

}

function newGame() {
    
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
    const element = document.getElementById('logo');
    element.remove();
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
function getSavedGame(s){
    fetch('/savegame',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({"session" : s})
        })
        .then((response) => response.json())
        .then((res) => {
                console.log(res);
                printSavedGame(res.board);
                mode = res.mode;
                sessionNum = s.substring(7); ;
                console.log(sessionNum);
                console.log(mode);
            })
}



function getSavedGames () {
    fetch('/saves',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({})
        })
        .then((response) => response.json())
        .then((res) => {
                joinGame(res.s1,res.s2,res.s3)
            })


}
function printSavedGame(board){
    startMenu.parentNode.removeChild(startMenu);

    createBoard();
    board.forEach((col, colIndex) =>{
        col.forEach((row, rowIndex) => {
            if (row === "p1"){
                document.getElementById(`col${colIndex}-row${rowIndex}`).classList.add("player-one");
            } else if (row === "p2") {
                document.getElementById(`col${colIndex}-row${rowIndex}`).classList.add("player-two");
            }
        });
    });
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
