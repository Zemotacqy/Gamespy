import numpy as np
import pandas as pd
from Player import Player
from Util import build_strategy_set, input_payoff

class Game:
    def __init__(self):
        print("""Game Setup:
              Enter Number of Players(n):
                Finite Positive Integer
              Strategies for each player (Array of strings without spaces):
                ['up', 'down', 'left', 'right']
              Provide Payoffs for all strategy_profiles(s1, s2, ... sn):
                n space separated real numbers""")
        self.players = []
        self.strategy_sets = pd.DataFrame({})
        self.utilities = pd.DataFrame({})

    def setup(self):
        n = int(input("Enter number of players: "))

        for i in range(n):
            player_strategies = input(f"Enter Strategies for Player {i}: ").lower().split(" ")
            self.players.append(Player(id = i, strat = player_strategies))
        
        self.strategy_sets = build_strategy_set(self.players) # Build strategy set for All Players

        print("Enter Payoff for each strategy Profile:")
        payoffs = []
        for _, strategy_profile in self.strategy_sets.iterrows():
            payoff = input_payoff(f"{strategy_profile}: ", n)
            payoffs.append(payoff)
        
        self.utilities = pd.DataFrame(payoffs, columns=[f"payoff_{col}" for col in self.strategy_sets.columns])
        self.utilities = pd.concat([self.strategy_sets, self.utilities], axis = 1)

        for index, pl in enumerate(self.players):
            pl.strategy_set_excluded = build_strategy_set(self.players[:index] + self.players[index+1:])
            # pl.build_correlated_beliefs() or pl.build_independent_beliefs()
    
    def find_dominated_strategies(self):
        for pl in self.players:
            print(f"\nFor Player: {pl.id}")
            pl.find_dominated_strategies(self.utilities)

    def view(self):
        print(f"{len(self.players)} Players")
        print(self.utilities)

def main():
    game = Game()
    game.setup()
    game.view()
    game.find_dominated_strategies()

if __name__ == "__main__":
    main()