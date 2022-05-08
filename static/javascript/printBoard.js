let finished = false;
let board=document.querySelector(".board")


createBoard()

//createBoard function
function createBoard(){
    let y = 5;
    for(let i = 0; i < 42; i++){
        let div = document.createElement("div");
        div.setAttribute("data-id", i);
        div.className = "square";

        let x = i % 7;
        div.id = `col${x}-row${y}`
        div.addEventListener('click', () => {
            sendPos(x*100+6, x);
        });

        board.appendChild(div)

        if (x === 6) {
            y--;
        }
    }
}

const sendPos = (col) => {
    let body = {
        x: col,
        session: sessionNum
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
                        } else {
                            document.getElementById(`col${res.pos[0]}-row${res.pos[1]}`).classList.add("player-two");
                        }

                        finished = true;
                    } else if (!res.finished) {
                        if (res.p1) {
                            document.getElementById(`col${res.pos[0]}-row${res.pos[1]}`).classList.add("player-one");
                        } else {
                            document.getElementById(`col${res.pos[0]}-row${res.pos[1]}`).classList.add("player-two");
                            //document.getElementById(`col${res.col}-row${res.pos[1]}`).style.backgroundColor = "#ffeb3b";
                        }
                    }
                }
            });
}
