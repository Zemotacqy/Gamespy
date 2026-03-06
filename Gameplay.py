import numpy as np

from Game import Game
from Util import utility

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
        return iesds(game)
    else:
        return game

def pure_nash_equilibrium(game):
    """
    We do a brute force check on each strategy and see if unilateral deviation is feasible
    on this strategy profile. If for any player, any strategy deviation is feasible, not a NE
    """
    utilities = game.utilities
    strategy_sets = game.strategy_sets
    players = game.players
    print(f"\n{'*' * 10} Pure Strategy Nash Equilibria {'*' * 10}\n")

    for _, strategy_profile in strategy_sets.iterrows(): # For each strategy profile

        for pl in players:  # Fix pl's strategy
            s_minus_i = strategy_profile.drop(pl.id)
            s_i = strategy_profile[pl.id]
            pl_curr_util = utility(s_i, s_minus_i, pl.id, utilities)
            deviation = False

            for s_i_deviated in pl.strategy[~np.isin(pl.strategy, s_i)]: # pl's strategy deviated
                pl_deviated_util = utility(s_i_deviated, s_minus_i, pl.id, utilities)
                if pl_deviated_util > pl_curr_util: # Deviation occurs, not a NE
                    deviation = True
                    break

            if deviation == False:
                print(strategy_profile, f"\nPayoff: {pl_curr_util}\n")
                break

def main():
    game = Game()
    game.load("./csv/game3.csv")
    game.view()
    iesds(game)
    pure_nash_equilibrium(game)

if __name__ == "__main__":
    main()