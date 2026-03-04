import numpy as np
import pandas as pd
from itertools import combinations

from Util import input_strategy_belief, utility

class Player:
    def __init__(self, id, strat):
        self.id = id
        self.strategy = np.array(strat, dtype=str)
        self.strategy_set_excluded = pd.DataFrame({})
        self.belief = pd.DataFrame({})
    
    def build_correlated_beliefs(self):
        beliefs = []
        available_belief = 1
        for _, strategy_profile in self.strategy_set_excluded.iterrows():
            probability = input_strategy_belief(strategy_profile, available_belief)            
            available_belief -= probability
            beliefs.append(probability)

        if sum(beliefs) != 1:
            print(f"Invalid Correlated Beliefs Built. Sum: {sum(beliefs)}. Try Again!!")
            self.build_correlated_beliefs(self)

        self.belief = pd.DataFrame(beliefs)
        self.strategy_set_excluded = pd.concat([self.strategy_set_excluded, self.belief], axis=1)

    def build_independent_beliefs(self):
        beliefs = []
        strat_probability = []
        for strat in self.strategy:
            strat_probability.append(input_strategy_belief(strat, 1))
        
        strat_beliefs = pd.DataFrame({
            "strategy": self.strategy,
            "probability": strat_probability
        })
        
        for _, strategy_profile in self.strategy_set_excluded.iterrows():
            belief = 1
            for strat in strategy_profile:
                belief = belief * strat_beliefs[strat]
            beliefs.append(belief)
        
        self.belief = pd.DataFrame(beliefs)
        self.strategy_set_excluded = pd.concat([self.strategy_set_excluded, self.belief], axis=1)

    def find_dominated_strategies(self, utilities):
        for s_i, s_j in list(combinations(self.strategy, 2)):
            i_minus_j = []
            for row in self.strategy_set_excluded.iterrows():
                s_minus_i = row[1] # row is a tuple, row[1] is a pd.Series
                u_s_i = utility(s_i, s_minus_i, self.id, utilities)
                u_s_j = utility(s_j, s_minus_i, self.id, utilities)
                
                i_minus_j.append(u_s_i - u_s_j)
            
            if np.all(np.array(i_minus_j) > 0):
                print(f"Strategy: {s_i} dominates {s_j}")
            elif np.all(np.array(i_minus_j) < 0):
                print(f"Strategy: {s_j} dominates {s_i}")