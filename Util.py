import numpy as np
import pandas as pd

def build_strategy_set(players):
    player_strategies = []
    player_index = []
    for pl in players:
        player_strategies.append(pl.strategy)
        player_index.append(pl.id)

    grids = np.meshgrid(*player_strategies)
    cartesian = np.column_stack([np.ravel(grid) for grid in grids])
    return pd.DataFrame(cartesian, columns=player_index)

def utility(s_i, s_minus_i, player_id, utilities):
    index_labels = s_minus_i.index.tolist()
    query = ""
    for pl_id in index_labels:
        query += f"`{pl_id}` == '{s_minus_i[pl_id]}' &"
    query += f" `{player_id}` == '{s_i}'"
    
    row = utilities.query(query)
    return row[f"payoff_{player_id}"].iloc[0]

def input_strategy_belief(input_text, available_belief):
    while True:
        probability = float(input(f"Probability for {input_text}: "))
        if probability <= available_belief:
            break
        else:
            print(f"Invalid Belief, Available Belief: {available_belief}. Try Again!!")
    return probability

def input_payoff(input_text, num_players):
    while True:
        payoff = input(input_text).split(" ")
        payoff = np.array(payoff, dtype=float)
        if len(payoff) == num_players:
            break
        else:
            print(f"Enter payoffs for {num_players} players.")
    return payoff
