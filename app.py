from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""



    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    board = game.board

    game_info = {'game_id': game_id, 'board': board}

    return jsonify(game_info)


@app.post("/api/score-word")
def is_word_legal():#add example for an accurate request : key / type, and return
    """ function accepts a post request with JSON for the game ID and the
    target word. checks if the word is in the word list, and exists on board"""

    word = request.json["word"].upper()
    game_id = request.json["gameId"]
    game = games[game_id]



    if not game.is_word_in_word_list(word):
        return jsonify(result="not-word")

    elif not game.check_word_on_board(word):
        return jsonify(result="not-on-board")

    else:
        game.play_and_score_word(word)
        return jsonify(result="ok")







