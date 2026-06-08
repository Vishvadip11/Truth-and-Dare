import json
import random
import itertools

random.seed(42)

with open('online_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Reset back to original small lists so we don't end up with duplicate appends on rerunning the script
for cat in data:
    data[cat]["truths"] = data[cat]["truths"][:20]
    data[cat]["dares"] = data[cat]["dares"][:20]

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

# 1. Popular Online
def pop_t_gen():
    adjs = ["most embarrassing", "weirdest", "funniest", "most awkward", "silliest", "most cringey", "most secret", "most random", "most annoying", "worst"]
    items = ["text message", "photo", "Google search history item", "app", "browser tab open", "screenshot", "video in gallery", "notification", "meme"]
    contexts = ["on your phone right now", "from today", "from this week", "from your childhood", "shared with your best friend", "on your social media", "received in the last 24 hours"]
    for a, i, c in itertools.product(adjs, items, contexts):
        yield f"What is the {a} {i} {c}?"

def pop_d_gen():
    media = [
        "screenshot of your screen time",
        "voice note of you singing a song chosen by me",
        "funny selfie using a weird filter",
        "screenshot of your last 3 WhatsApp chats",
        "photo of the nearest object to your left",
        "voice note explaining why water is wet in a funny accent",
        "screenshot of your search history",
        "screenshot of your Instagram Direct Messages list",
        "voice note speaking like a news reporter about what you did today",
        "funny face selfie",
        "screenshot of your home screen",
        "photo of what you are wearing right now",
        "voice note whispering a nursery rhyme",
        "screenshot of your recently played songs",
        "photo of your feet or hands",
        "voice note saying 'I love you' in a cartoon voice"
    ]
    actions = [
        "send it to the other player right now",
        "post it as your WhatsApp status for 15 minutes",
        "send it to your best friend and share their reaction screenshot",
        "text it to a random group chat you are in",
        "send it to your cousin and tell them it was an accident",
        "post it as your Instagram story for 1 hour",
        "send it to the third contact on your chat list",
        "send it to your parent and say 'sorry, wrong person'"
    ]
    for m, a in itertools.product(media, actions):
        yield f"Please take a {m} and {a}."

# 2. Xtreme Online
def xtreme_t_gen():
    actions = [
        "stalked an ex online for hours",
        "created a fake social media profile to spy on someone",
        "sent a text by mistake to your boss/teacher",
        "cheated in an online exam or test",
        "lied about your relationship status to someone online",
        "ghosted someone you were talking to online",
        "shared a private chat screenshot with someone else",
        "sent a message you regret deeply to a crush",
        "deleted your social media account to avoid someone",
        "pretended to be someone else in a chatroom",
        "lied about your age or location to someone online",
        "spent money online that you did not have",
        "downloaded an app and deleted it because it was too weird",
        "sent a text to your boss/teacher while half asleep",
        "shared a secret you promised never to tell"
    ]
    contexts = [
        "and never felt guilty about it",
        "and got caught red-handed",
        "to save your reputation",
        "just for fun",
        "and regretted it immediately",
        "because you were bored",
        "to make someone jealous",
        "to see how they would react",
        "without telling your friends"
    ]
    for a, c in itertools.product(actions, contexts):
        yield f"Have you ever {a} {c}?"

def xtreme_d_gen():
    texts = [
        "'I am in love with you.'",
        "'I know your secret.'",
        "'Can we get married tomorrow?'",
        "'I am leaving the country today.'",
        "'Please don't contact me again.'",
        "'I accidentally deleted all my files, help!'",
        "'I think we need to talk.'",
        "'I am a secret agent on a mission.'",
        "'Did you see that ghost behind you?'",
        "'I need a favor, please don't ask questions.'",
        "'I can't stop thinking about you.'",
        "'Why did you do this to me?'"
    ]
    recipients = [
        "your crush",
        "your ex",
        "the 3rd person on your WhatsApp contact list",
        "a random contact on your phone list",
        "your best friend",
        "the most recent person you chatted with",
        "your sibling",
        "your cousin",
        "the 5th contact on your list",
        "someone you haven't spoken to in over a year"
    ]
    for t, r in itertools.product(texts, recipients):
        yield f"Text {r} {t} and send a screenshot of their response here."

# 3. Couple Online
def couple_t_gen():
    adjs = ["most romantic", "sweetest", "most cherished", "funniest", "cutest", "warmest", "favorite", "deepest", "most passionate", "silliest"]
    nouns = ["text message", "voice note", "memory", "virtual date moment", "dream", "fantasy", "secret", "thought", "regret", "wish"]
    contexts = [
        "we have ever shared",
        "from our first week of talking",
        "about our future together",
        "on our video calls",
        "that you haven't told me yet",
        "about my personality",
        "when you look at my photos",
        "about the first time we kissed/held hands"
    ]
    for a, n, c in itertools.product(adjs, nouns, contexts):
        yield f"What is the {a} {n} {c}?"

def couple_d_gen():
    actions = [
        "Send a voice note whispering 'I love you' in a cute voice",
        "Send a selfie blowing a kiss to me",
        "Write a 4-line romantic poem for me right now",
        "Set your status to 'In a relationship with my favorite person'",
        "Change your lockscreen wallpaper to a photo of us/me",
        "Send a voice note singing our favorite song",
        "Text me 5 things you find most attractive about me",
        "Draw a digital sketch of me and send it",
        "Send a voice message describing your perfect date with me",
        "Whisper your favorite secret about us in a voice note",
        "Send a video of you blowing 3 different kisses",
        "Text me a cheesy pickup line in a dramatic way",
        "Send a photo of you wearing my favorite color",
        "Send a voice note describing me using only 5 sweet adjectives",
        "Text me a message saying 'You are my favorite notification'",
        "Send a selfie holding a piece of paper that says 'I love you'",
        "Change your WhatsApp status to a heart emoji"
    ]
    durations = [
        "right now",
        "for 1 hour",
        "for 2 hours",
        "until the game ends",
        "for the rest of the day",
        "for the next 24 hours",
        "until tomorrow morning"
    ]
    for a, d in itertools.product(actions, durations):
        yield f"{a} {d}."

# 4. Spicy Online
def spicy_t_gen():
    adjs = ["wildest", "most daring", "hottest", "most secret", "most seductive", "most intimate", "most scandalous", "most forbidden", "dirtiest", "most thrilling", "sexiest", "most teasing", "most private"]
    topics = [
        "fantasy you've never told anyone",
        "thought you had about me recently",
        "text you have sent to someone in secret",
        "photo you have on your phone right now",
        "dream you had about the other player",
        "turn-on that you are embarrassed of",
        "place you've ever had a romantic encounter",
        "habit you have when you are alone in your room",
        "thing that turns you on instantly",
        "crush you've had on someone online",
        "thing you find irresistible in a partner",
        "memory of a spicy dream you woke up from"
    ]
    for a, t in itertools.product(adjs, topics):
        yield f"What is the {a} {t}?"

def spicy_d_gen():
    actions = [
        "Send a voice note describing your favorite fantasy in a low, whispering voice",
        "Send a close-up photo of your lips or collarbone",
        "Send a flirty text message to the other player right now",
        "Whisper a dirty joke or pickup line in a voice note",
        "Send a photo of you biting your lower lip",
        "Send a voice note describing what you find most attractive about me",
        "Send a photo of your bare shoulder or neck",
        "Wink slowly at the camera in a short 5-second video",
        "Text your partner/crush 'I want you right now' and screenshot the reaction",
        "Tell me a secret in a sensual, deep voice note",
        "Send a selfie wearing your most attractive shirt/outfit",
        "Describe what you would do if we were in the same room right now",
        "Blow a slow, seductive kiss on video",
        "Text your crush 'You looked great today' out of nowhere"
    ]
    conditions = [
        "making it sound very attractive",
        "in under 30 seconds",
        "right now",
        "with a winking emoji",
        "in a deep voice",
        "without laughing",
        "in a slow whisper",
        "with a smile",
        "in a serious tone"
    ]
    for a, c in itertools.product(actions, conditions):
        yield f"{a} {c}."

# 5. Kids Online
def kids_t_gen():
    items = [
        "cartoon character", "video game", "animal", "superhero", "toy", "movie", "school subject", 
        "food", "holiday destination", "planet", "mythical creature", "board game", "book", 
        "hobby", "ice cream flavor", "funny word", "sport", "season", "song", "historical figure"
    ]
    questions = [
        "would you want to be", "is your favorite", "would you want to meet in real life", 
        "do you like the most", "would you delete from existence", "do you think is the coolest",
        "makes you laugh the most", "is the most boring"
    ]
    for i, q in itertools.product(items, questions):
        yield f"Which {i} {q} and why?"

def kids_d_gen():
    animals = ["monkey", "cat", "dog", "dinosaur", "frog", "lion", "elephant", "duck", "chicken", "cow", "rabbit", "bear", "snake", "mouse", "giraffe", "kangaroo"]
    actions = [
        "making their funny sound",
        "eating their favorite food",
        "doing a silly dance",
        "running around in circles",
        "taking a lazy nap",
        "giving a lecture",
        "brushing their teeth",
        "crying like a baby"
    ]
    for a, act in itertools.product(animals, actions):
        yield f"Send a video/voice note of you acting like a {a} {act}."

# 6. Office Online
def office_t_gen():
    actions = [
        "played games during an online meeting",
        "pretended your mic or camera wasn't working to avoid speaking",
        "sent a funny message to the wrong coworker",
        "taken a nap during work hours",
        "gossiped about your manager with a coworker",
        "online shopped during work hours",
        "muted a meeting to watch a video",
        "lied about your workload to get free time",
        "joined an online meeting while still in bed",
        "made a mistake at work and blamed the system/network",
        "taken a sick leave when you were perfectly fine",
        "slacked a coworker about someone else on the same call",
        "ignored a direct message from your boss for hours",
        "pretended to be extremely busy to avoid extra tasks"
    ]
    conditions = [
        "while working from home",
        "and got caught by someone",
        "without anyone knowing",
        "on a busy Monday morning",
        "during a client call",
        "right before a weekend",
        "to attend a movie or video game release",
        "to go out with friends",
        "because you were feeling too lazy to work"
    ]
    for a, c in itertools.product(actions, conditions):
        yield f"Have you ever {a} {c}?"

def office_d_gen():
    actions = [
        "Change your Slack/Teams status to 'Sleeping'",
        "Send a corporate buzzword-filled message",
        "Draft a funny resignation letter",
        "Write a 2-line funny rhyme about work",
        "Take a selfie with a cup of coffee looking super busy",
        "Draft an out-of-office message saying you are on a secret mission",
        "Translate a simple corporate email into teenager slang",
        "Send a message saying 'Let's synergize our touchpoints offline'",
        "Draft an email to your colleague praising their typing speed",
        "Send a Slack update using only emojis to describe your day",
        "Send a screenshot of your current browser bookmark bar",
        "Record a voice message saying 'Let me loop in my cat for alignment'",
        "Create a fake calendar meeting named 'alignment session'",
        "Change your avatar to a funny coffee cup drawing",
        "Write 'Under construction, check back later' in your bio"
    ]
    targets = [
        "to the other player right now",
        "and take a screenshot of it",
        "for 10 minutes",
        "and share it as a status update",
        "and send it to a close colleague",
        "and delete it after 1 minute",
        "right before the game ends",
        "and ask for feedback"
    ]
    for a, t in itertools.product(actions, targets):
        yield f"{a} {t}."

add_unique("popular", "truths", pop_t_gen(), count=100)
add_unique("popular", "dares", pop_d_gen(), count=100)
add_unique("xtreme", "truths", xtreme_t_gen(), count=100)
add_unique("xtreme", "dares", xtreme_d_gen(), count=100)
add_unique("couple", "truths", couple_t_gen(), count=100)
add_unique("couple", "dares", couple_d_gen(), count=100)
add_unique("spicy", "truths", spicy_t_gen(), count=100)
add_unique("spicy", "dares", spicy_d_gen(), count=100)
add_unique("kids", "truths", kids_t_gen(), count=100)
add_unique("kids", "dares", kids_d_gen(), count=100)
add_unique("office", "truths", office_t_gen(), count=100)
add_unique("office", "dares", office_d_gen(), count=100)

with open('online_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Successfully added 100 extra questions to online_data.json!")
