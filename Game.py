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

    # Manually input payoffs and strategies
    def setup(self):
        n = int(input("Enter number of players: "))

        for i in range(n):
            player_strategies = input(f"Enter Strategies for Player {i}: ").lower().split(" ")
            self.players.append(Player(id = i, strat = player_strategies))
        
        self.strategy_sets = build_strategy_set(self.players) # Build strategy set for All Players
        self.setup_players()

        print("Enter Payoff for each strategy Profile:")
        payoffs = []
        for _, strategy_profile in self.strategy_sets.iterrows():
            payoff = input_payoff(f"{strategy_profile}: ", n)
            payoffs.append(payoff)
        
        self.utilities = pd.DataFrame(payoffs, columns=[f"payoff_{col}" for col in self.strategy_sets.columns])
        self.utilities = pd.concat([self.strategy_sets, self.utilities], axis = 1)

    # Load strategies and payoffs from csv file
    def load(self, path):
        self.utilities = pd.read_csv(path)
        players = [c for c in self.utilities.columns if c.isnumeric()]
        for player_id in players:
            strategies = self.utilities.loc[:, player_id].unique()
            self.players.append(Player(id = player_id, strat = strategies))

        self.setup_players()

    def setup_players(self):
        self.strategy_sets = build_strategy_set(self.players) # Build strategy set for All Players

        for index, pl in enumerate(self.players):
            pl.strategy_set_excluded = build_strategy_set(self.players[:index] + self.players[index+1:])
            # pl.build_correlated_beliefs() or pl.build_independent_beliefs()
            # TODO: We dont want to update beliefs at each iteration of deletions

    def remove_strategy(self, strat, player_id):
        # Remove the rows where the player plays strat
        self.utilities = self.utilities[~(self.utilities[player_id] == strat)]

    def view(self):
        print(f"{len(self.players)} Players")
        print(self.utilities)

def main():
    game = Game()
    game.load("./csv/game1.csv") # or game.setup()
    game.view()

if __name__ == "__main__":
    main()