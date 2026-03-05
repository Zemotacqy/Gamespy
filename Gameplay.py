import numpy as np
import pandas as pd

from Game import Game

def iesds(game):
    utilities = game.utilities
    players = game.players
    strategies_deleted = 0

    for pl in players:
        dominated_strategies = pl.find_dominated_strategies(utilities)
        if len(dominated_strategies) > 0:
            _, b = dominated_strategies[0] # b is strictly dominated, player will never play b
            print(f"Removing strategy {b} for player {pl.id}")
            pl.remove_strategy(b)
            game.remove_strategy(b, pl.id)
            game.setup_players()
            strategies_deleted += 1

    game.view()
    if strategies_deleted > 0:
        iesds(game)

def main():
    game = Game()
    game.load("./csv/game2.csv")
    game.view()
    iesds(game)

if __name__ == "__main__":
    main()