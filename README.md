# Python3 Minigames

Simple Minigames developed in Python.

The Minigames are based on classes, so you can extend them, use them to learn programming or build your own bots and algorithms to play against you, your friends and their bots.

There are currently six minigames:
- 2048 (`2048.py`)
- Chess (`chess.py`)
- Flip 7 (`flip7.py`)
- Four in a Row (`fourinarow.py`)
- TicTacToe (`tictactoe.py`)
- Wordle (`wordle.py`)
    - **Wordle Word List:** https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93

There are currently two bots:
- TicTacToe-Bot (`tictactoe_bot.py`)
    - **Warning:** Poor code and no comments
    - Statistics as X (against random moves): 98.7% Wins; 01.3% Remis; 00.0% Lose
    - Statistics as O (against random moves): 86.7% Wins; 13.3% Remis; 00.0% Lose
    - **Info:** Change `PLAYER` in line 3 to `'X'` (if you want to start) or `'O'` (if you want the bot to start)
- learning TicTacToe-Bot (`tictactoe_bot_learning.py`)
    - Statistics as X (against random moves): 98.9% Wins; 01.1% Remis; 00.0% Lose
    - Statistics as O (against random moves): 90.0% Wins; 10.0% Remis; 00.0% Lose
        - **Attention:** the bot is only this good if it uses the data from `ttt_bot.data`
        - may increase through learning (run `tictactoe_bot_learning_learn.py`)
    - **Info:** Change `PLAYER` in line 3 to `'X'` (if you want to start) or `'O'` (if you want the bot to start)


There are currently five bot templates:
- 2048 (`2048_bot_template.py`)
- Chess-Bot-Template (`chess_bot_template.py`)
- Four In A Row-Bot-Template (`fourinarow_bot_template.py`)
- TicTacToe-Bot-Template (`tictactoe_bot_template.py`)
- Wordle-Bot-Template (`wordle_bot_template.py`)