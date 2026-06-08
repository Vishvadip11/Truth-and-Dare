import random
import json

def load_data(online=False):
    filename = "online_data.json" if online else "data.json"
    with open(filename, encoding="utf-8") as f:
        return json.load(f)

def get_truth(category="popular", online=False):
    data = load_data(online)
    cat = data.get(category, data["popular"])
    return random.choice(cat["truths"])

def get_dare(category="popular", online=False):
    data = load_data(online)
    cat = data.get(category, data["popular"])
    return random.choice(cat["dares"])

# Multiplayer
def next_player(players, current_index):
    return (current_index + 1) % len(players)