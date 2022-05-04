let finished = false
const canvas = document.getElementById("my-canvas")
const context = canvas.getContext("2d")
board.onload = () => {
  context.drawImage(board, 0, 0)
}

function getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top
    sendPos(x)
}

const myCanvas = document.querySelector('#my-canvas')
myCanvas.addEventListener('mousedown', function(e) {
    getCursorPosition(myCanvas, e)
})

const sendPos = (x) => {
    let body = {
        x: x,
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
                        context.drawImage(chip1, res.pos[0], res.pos[1])
                    } else {
                        context.drawImage(chip2, res.pos[0], res.pos[1])
                    }
                    finished = true
                } else if (!res.finished) {
                    if (res.p1) {
                        context.drawImage(chip1, res.pos[0], res.pos[1])
                    } else {
                        context.drawImage(chip2, res.pos[0], res.pos[1])
                    }
                }
            }
        })
}
