# import pygame
import model
import ai
import math
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.get("/")
def gameLoop():
    # pygame.init()
    input = request.args.get("tiles", default="1 2 3 0 4 6 7 5 8")
    formatted = [int(x) for x in input.split(" ")]
    BOARD_SIZE = int(math.sqrt(len(formatted)))
    NANO_TO_SEC = 1000000000

    # ai
    ai.init(BOARD_SIZE)
    aiMoveIndex = 0
    aiMoves = []

    # movements
    UP = (1,0)
    DOWN = (-1,0)
    LEFT = (0,1)
    RIGHT = (0,-1)
    MOVES = {
        UP: "Up",
        DOWN: "Down",
        LEFT: "Left",
        RIGHT: "Right"
    }

    # test = [[3,4,5], [0,8,7], [6,2,1]]
    # test = [[1,2,3], [4,0,5], [7,8,6]]
    test = to_matrix(formatted, BOARD_SIZE)

    puzzle = model.Puzzle(boardSize=BOARD_SIZE, shuffle=False, test=test)
    aiMoves = ai.idaStar(puzzle)
    RESULT = []
    for item in aiMoves:
        RESULT.append(MOVES[item])
    return(", ".join(move for move in RESULT))

def to_matrix(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

if __name__ == "__main__":
    # Development only: run "python main.py" and open http://localhost:8080
    # When deploying to Cloud Run, a production-grade WSGI HTTP server,
    # such as Gunicorn, will serve the app.
    app.run(host="localhost", port=8080, debug=True)
