from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed.
        Checks for rendering of Boggle board, and response code 200
        """

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('this template was successfully rendered' ,html)
            ...
            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game. Route returns JSON with a game id, and a
        list of lists for the board. board is stored in games dictionary.

        """

        with self.client as client:
            response = client.post("/api/new-game")
            data = response.get_json()

            game_id = data.get('game_id')
            board = data.get('board')

            self.assertTrue(isinstance(game_id, str))
            self.assertTrue(isinstance(board, list))
            # self.assertTrue(isinstance(board, list))

            self.assertIn(game_id, games)

            ...


    def test_score_word(self):
        """tests whether word scoring works. word should be valid, on board,
        or return ok. test creates new temporary board for testing, and
        iterates over the board. """

        with self.client as client:
            response = client.post("/api/new-game")
            data = response.get_json()


            game_id = data.get('game_id')
            game = games[game_id]

            # change board

            game.board[0] = ["X", "X", "X", "X", "X"]
            game.board[1] = ["X", "X", "X", "X", "C"]
            game.board[2] = ["D", "O", "G", "A", "X"]
            game.board[3] = ["X", "X", "X", "X", "T"]
            game.board[4] = ["X", "X", "X", "X", "X"]


            response = self.client.post(
                "/api/score-word",
                json = {"word": "CAT", "game_id" : game_id})

            self.assertEqual(response.get_json(), {'result': 'ok'})

            response = self.client.post(
                "/api/score-word",
                json = {"word": "DOG", "game_id" : game_id})

            self.assertEqual(response.get_json(), {'result': 'ok'})

            response = self.client.post(
                "/api/score-word",
                json={"word": "TATEGER", "game_id": game_id})
            self.assertEqual(response.get_json(), {'result': 'not-word'})

            response = self.client.post(
                "/api/score-word",
                json={"word": "APPLE", "game_id": game_id})
            self.assertEqual(response.get_json(), {'result': 'not-on-board'})

            ...








