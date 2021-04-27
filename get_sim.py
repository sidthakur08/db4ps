import json

with open('gamestop/games.txt','r') as f:
    games = json.load(f)
with open('gamestop/game_vector.txt','r') as f:
    game_vector = json.load(f)

def get_sim(a,b):
    return 1-spatial.distance.cosine(game_vector[a],game_vector[b])

def get_5_sim(to_search):
    sim_measure = []
    for i in game_vector.keys():
        try:
            sim_measure.append(get_sim(to_search,i))
        except:
            sim_measure.append(0)
    sorted_sim_measure = np.argsort(sim_measure)[-6:-1][::-1]
    sim_games = [(games[s]['Name'],sim_measure[s]) for s in sorted_sim_measure]
    return sim_games

print(game_vector[0])