import json
import random
import itertools

random.seed(42)

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def add_unique(category, q_type, generator, count=100):
    existing = set(data[category][q_type])
    added = 0
    generated = list(generator)
    random.shuffle(generated)
    for q in generated:
        if added >= count:
            break
        if q not in existing:
            data[category][q_type].append(q)
            existing.add(q)
            added += 1
    print(f"{category} {q_type}: total {len(data[category][q_type])}")

# 1. Popular
def pop_t_gen():
    adjs = ["most embarrassing", "weirdest", "funniest", "darkest", "strangest", "most awkward", "silliest"]
    nouns = ["memory", "secret", "habit", "thought", "dream", "fantasy", "confession"]
    topics = ["your childhood", "school", "your friends", "your family", "dating", "yourself", "strangers"]
    for a, n, t in itertools.product(adjs, nouns, topics):
        yield f"What is your {a} {n} about {t}?"

def pop_d_gen():
    durations = ["the next 2 rounds", "1 minute", "30 seconds", "the rest of the game", "3 rounds"]
    actions = ["speak in an accent", "hold your breath", "stand on one leg", "keep your eyes closed", "talk like a baby", "whisper", "shout everything"]
    conditions = ["patting your head", "holding the person to your left's hand", "staring at the ceiling", "making weird faces", "doing jumping jacks"]
    for d, a, c in itertools.product(durations, actions, conditions):
        yield f"For {d}, you must {a} while {c}."

# 2. Xtreme
def xtreme_t_gen():
    actions = ["stolen something valuable", "broken the law", "lied to get someone in trouble", "betrayed a deep secret", "ruined someone's life", "manipulated someone", "cheated in a major way", "faked an emergency", "sneaked into a restricted area", "hacked into an account", "destroyed property", "run away from home", "started a vicious rumor", "read someone's private diary", "eavesdropped on a life-changing conversation"]
    contexts = ["and never got caught", "and blamed it on a friend", "just for the thrill of it", "for money", "to get revenge", "without feeling any guilt", "and deeply regretted it"]
    for a, c in itertools.product(actions, contexts):
        yield f"Have you ever {a} {c}?"

def xtreme_d_gen():
    actions = ["eat a spoonful of", "lick", "smell", "bite into", "hold in your mouth", "chew on", "rub on your face", "put on your head"]
    targets = ["hot sauce", "raw onion", "mustard", "mayonnaise", "a lemon slice", "a raw potato", "black pepper", "cinnamon", "pickle juice", "soy sauce", "the bottom of a shoe", "a pet treat", "a piece of garlic", "coffee grounds", "vinegar"]
    for a, t in itertools.product(actions, targets):
        yield f"You must {a} {t}."

# 3. Couple
def couple_t_gen():
    adjs = ["favorite", "most cherished", "sexiest", "most romantic", "sweetest", "funniest", "most surprising"]
    nouns = ["memory", "thought", "fantasy", "dream", "secret", "desire", "confession"]
    contexts = ["about our first date", "about our first kiss", "about our future together", "about my physical appearance", "about my personality", "about our intimate life", "about the time we met"]
    for a, n, c in itertools.product(adjs, nouns, contexts):
        yield f"What is your {a} {n} {c}?"

def couple_d_gen():
    types = ["sensual massage", "passionate kiss", "gentle tickle", "loving stroke", "sweet kiss", "soft bite", "warm hug", "playful squeeze"]
    targets = ["on the neck", "on the back", "on the lips", "on the ear", "on the hand", "on the shoulder", "on the cheek", "on the jawline", "on the thigh"]
    durations = ["for 10 seconds", "for 30 seconds", "for 1 minute", "for 2 minutes", "until your next turn"]
    for t1, t2, d in itertools.product(types, targets, durations):
        yield f"Give your partner a {t1} {t2} {d}."

# 4. Spicy
def spicy_t_gen():
    adjs = ["biggest", "darkest", "most secret", "wildest", "most intense", "favorite", "most embarrassing"]
    nouns = ["turn-on", "fantasy", "experience", "regret", "desire", "kink", "curiosity"]
    topics = ["intimacy", "roleplay", "public displays of affection", "strangers", "friends", "exes", "toys", "weird places"]
    for a, n, t in itertools.product(adjs, nouns, topics):
        yield f"What is your {a} {n} regarding {t}?"

def spicy_d_gen():
    actions = ["Whisper something dirty", "Give a seductive look", "Do a sexy crawl", "Perform a lap dance", "Bite your lip", "Trace a heart", "Give a sensual massage", "Blow a kiss"]
    targets = ["to the person on your left", "to the person on your right", "to anyone you choose", "to the most attractive person here", "to the camera", "to the oldest person here"]
    conditions = ["making intense eye contact", "unbuttoning one piece of clothing", "playing with your hair", "winking slowly", "breathing heavily", "smiling seductively"]
    for a, t, c in itertools.product(actions, targets, conditions):
        yield f"{a} {t} while {c}."

# 5. Kids
def kids_t_gen():
    actions = ["have any", "be any", "eat only one", "play with one", "meet any", "travel to any"]
    objects = ["superpower", "animal", "candy", "toy", "cartoon character", "video game", "dinosaur", "planet"]
    outcomes = ["it be", "you choose", "you do first", "you tell your friends", "be your superhero name"]
    for a, o, out in itertools.product(actions, objects, outcomes):
        yield f"If you could {a} {o}, what would {out}?"

def kids_d_gen():
    animals = ["monkey", "dinosaur", "robot", "penguin", "frog", "cat", "dog", "bear", "bird", "fish"]
    activities = ["eating a banana", "dancing to music", "trying to fly", "waddling across the room", "looking for food", "taking a nap", "doing homework", "playing a video game", "brushing its teeth"]
    durations = ["for 10 seconds", "for 20 seconds", "for 30 seconds", "for 1 minute", "until everyone laughs"]
    for a, act, d in itertools.product(animals, activities, durations):
        yield f"Act like a {a} {act} {d}."

# 6. Office
def office_t_gen():
    actions = ["fallen asleep", "played games", "cried", "gossiped", "eaten someone's food", "lied to the boss", "faked sick", "stolen supplies", "browsed social media", "taken a personal call"]
    contexts = ["during a very important meeting", "while pretending to work", "in the bathroom", "at your desk", "on a Monday morning", "right before a deadline", "during a team lunch", "when you thought no one was watching", "on a video call with camera off", "in front of a client"]
    for a, c in itertools.product(actions, contexts):
        yield f"Have you ever {a} {c}?"

def office_d_gen():
    actions = ["Send an email", "Send a slack message", "Walk up to a coworker and say", "Stand up and announce", "During the next round, act like", "For the next 5 minutes, pretend"]
    roles = ["you are the CEO", "a random compliment", "a completely out-of-context quote", "that you just won the lottery", "a buzzword-filled sentence", "you are completely lost", "a robot trying to understand human work", "you lost your most important file", "you are giving a motivational speech"]
    targets = ["to your boss", "to the person on your right", "to the team chat", "to your favorite coworker", "to the person who spoke last"]
    for a, r, t in itertools.product(actions, roles, targets):
        yield f"{a} {r} {t}."


add_unique("popular", "truths", pop_t_gen())
add_unique("popular", "dares", pop_d_gen())
add_unique("xtreme", "truths", xtreme_t_gen())
add_unique("xtreme", "dares", xtreme_d_gen())
add_unique("couple", "truths", couple_t_gen())
add_unique("couple", "dares", couple_d_gen())
add_unique("spicy", "truths", spicy_t_gen())
add_unique("spicy", "dares", spicy_d_gen())
add_unique("kids", "truths", kids_t_gen())
add_unique("kids", "dares", kids_d_gen())
add_unique("office", "truths", office_t_gen())
add_unique("office", "dares", office_d_gen())

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Done generating extra 100 each!")
