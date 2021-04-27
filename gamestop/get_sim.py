import json

with open('games.txt','r') as f:
    b = json.load(f)

print(b)

def get_5_sim(to_search):
    sim_measure = []
    for i in game_vector.keys():
        try:
            sim_measure.append(get_sim(to_search,i))
        except:
            sim_measure.append(0)
    sorted_sim_measure = np.argsort(sim_measure)[-6:-1][::-1]
    sim_games = [(l[s]['Name'],sim_measure[s]) for s in sorted_sim_measure]
    return sim_games

