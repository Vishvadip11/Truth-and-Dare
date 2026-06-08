import streamlit as st
import random
from game import get_truth, get_dare
import base64
import os
import math
import time

# ---------- BACKGROUND FUNCTION ----------
def set_bg(image_file):
    if not os.path.exists(image_file):
        st.error(f"Image not found: {image_file}")
        return
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        top:0; left:0;
        width:100%; height:100%;
        background: rgba(0,0,0,0.5);
        z-index: 0;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------- PAGE ----------
st.set_page_config(page_title="Truth or Dare", layout="wide")



# ---------- SESSION ----------
if "screen" not in st.session_state:
    st.session_state.screen = "home"
if "players" not in st.session_state:
    st.session_state.players = []
if "current" not in st.session_state:
    st.session_state.current = ""
if "bottle_angle" not in st.session_state:
    st.session_state.bottle_angle = 0
if "winner_index" not in st.session_state:
    st.session_state.winner_index = -1
if "is_spinning" not in st.session_state:
    st.session_state.is_spinning = False
if "category" not in st.session_state:
    st.session_state.category = "popular"
if "mode" not in st.session_state:
    st.session_state.mode = "offline"
if "room_code" not in st.session_state:
    st.session_state.room_code = ""
if "my_name" not in st.session_state:
    st.session_state.my_name = ""
if "is_creator" not in st.session_state:
    st.session_state.is_creator = False
if "local_last_update" not in st.session_state:
    st.session_state.local_last_update = 0.0
if "online_action" not in st.session_state:
    st.session_state.online_action = ""

# ---------- MULTIPLAYER ROOMS ----------
@st.cache_resource
def get_rooms():
    return {}

# ---------- CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Rajdhani:wght@600;700&display=swap');

/* Global Font Overrides */
html, body, [class*="css"], .stMarkdown, p, div, label, span, input, button {
    font-family: 'Outfit', sans-serif !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 0rem !important;
    max-width: 1200px !important;
}

[data-testid="stHeader"] {
    display: none !important;
}

/* Styled Title */
.title {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 60px !important;
    font-weight: 800 !important;
    text-align: center;
    background: linear-gradient(90deg, #ff00cc, #9d4edd, #00d4ff) !important;
    -webkit-background-clip: text !important;
    color: transparent !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 5px !important;
    animation: neonPulse 3s infinite alternate;
}

@keyframes neonPulse {
    0% { filter: drop-shadow(0 0 4px rgba(255, 0, 204, 0.4)); }
    100% { filter: drop-shadow(0 0 12px rgba(0, 212, 255, 0.6)); }
}

.center { text-align: center; }

/* Hide default streamlit audio player */
div[data-testid="stAudio"], audio {
    display: none !important;
}

/* Glassmorphism/Borders removed per user request */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    padding: 10px !important;
}

/* Form inputs styling with transparent backgrounds to prevent black boxes */
.stTextInput input {
    background-color: rgba(255, 255, 255, 0.05) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 16px !important;
    padding: 12px 20px !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
}
.stTextInput input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.4) !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
}
.stTextInput input::placeholder {
    color: rgba(255, 255, 255, 0.4) !important;
}
.stTextInput label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* Divider lines */
hr {
    border: 0 !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent) !important;
    margin: 25px 0 !important;
}

/* Lobby player rows */
.player-row {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 12px 20px;
    border-radius: 14px;
    color: white;
    font-size: 18px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    transition: all 0.2s ease;
}
.player-row:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateX(4px);
    border-color: rgba(0, 212, 255, 0.2);
}

/* Base button styling overrides */
.stButton > button {
    border-radius: 30px !important;
    padding: 12px 28px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
}
.stButton > button:active {
    transform: translateY(1px) scale(0.98) !important;
}

/* Primary Button (Gold/Orange gradient) */
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #ffd200, #ff6a00) !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(255, 106, 0, 0.3) !important;
}
button[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, #ff6a00, #ffd200) !important;
    box-shadow: 0 8px 25px rgba(255, 106, 0, 0.6) !important;
    color: #0f172a !important;
}

/* Secondary Button (Dark purple/pink) */
button[data-testid="baseButton-secondary"] {
    background: linear-gradient(135deg, #1e1b4b, #311042) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
}
button[data-testid="baseButton-secondary"]:hover {
    background: linear-gradient(135deg, #ff00cc, #7f00ff) !important;
    border-color: transparent !important;
    box-shadow: 0 6px 20px rgba(255, 0, 204, 0.4) !important;
    color: white !important;
}
</style>

""", unsafe_allow_html=True)

# ---------- SCREEN 1 ----------
if st.session_state.screen == "home":
    set_bg("photos/frist.png")

    st.markdown('<div class="title">Truth or Dare</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="center" style="
        font-size:20px;
        font-weight:600;
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        color: transparent;
        letter-spacing: 1px;
    ">
    Ultimate Party Game 🎉
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔥 Let's Play", use_container_width=True, type="primary"):
            st.session_state.screen = "mode_selection"
            st.rerun()

# ---------- SCREEN: MODE SELECTION ----------
elif st.session_state.screen == "mode_selection":
    set_bg("photos/second.png")
    st.markdown('<div class="title">Select Mode</div>', unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=False):
            st.markdown("<p style='text-align:center; color:#cbd5e1; font-size:16px; margin-bottom:20px;'>Choose how you want to play:</p>", unsafe_allow_html=True)
            
            if st.button("📱 Play Offline (Same Phone)", use_container_width=True, type="primary"):
                st.session_state.mode = "offline"
                st.session_state.screen = "players"
                st.rerun()
                
            if st.button("🌐 Play Online (Different Phones)", use_container_width=True, type="primary"):
                st.session_state.mode = "online"
                st.session_state.screen = "online_setup"
                st.session_state.online_action = ""
                st.rerun()
                
            if st.button("Back to Menu", use_container_width=True):
                st.session_state.screen = "home"
                st.rerun()

# ---------- SCREEN: ONLINE SETUP ----------
elif st.session_state.screen == "online_setup":
    set_bg("photos/second.png")
    
    if st.session_state.online_action == "create":
        st.markdown('<div class="title">Host Game</div>', unsafe_allow_html=True)
    elif st.session_state.online_action == "join":
        st.markdown('<div class="title">Join Game</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="title">Online Setup</div>', unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.online_action == "":
            st.markdown("<p style='text-align:center; color:#cbd5e1; font-size:16px; margin-bottom:20px;'>Select whether you want to host a new room or join an existing game:</p>", unsafe_allow_html=True)
            
            if st.button("👑 Host Game (Create Room)", use_container_width=True, type="primary"):
                st.session_state.online_action = "create"
                st.rerun()
                
            if st.button("🤝 Join Game (Enter Code)", use_container_width=True, type="primary"):
                st.session_state.online_action = "join"
                st.rerun()
                
            st.write("")
            if st.button("Back", key="back_setup", use_container_width=True):
                st.session_state.screen = "mode_selection"
                st.rerun()
                
        elif st.session_state.online_action == "create":
            st.markdown("<p style='text-align:center; color:#cbd5e1; font-size:15px; margin-bottom:15px;'>Enter your name to create a game room:</p>", unsafe_allow_html=True)
            my_name = st.text_input("Your Name", placeholder="Your name...", key="my_name_input_host").strip()
            
            st.write("")
            if st.button("Create New Room", use_container_width=True, type="primary"):
                if not my_name:
                    st.error("Please enter your name first!")
                else:
                    rooms = get_rooms()
                    room_code = str(random.randint(1000, 9999))
                    while room_code in rooms:
                        room_code = str(random.randint(1000, 9999))
                    
                    rooms[room_code] = {
                        "players": [my_name],
                        "current": my_name,
                        "bottle_angle": 0,
                        "winner_index": -1,
                        "is_spinning": False,
                        "category": "popular",
                        "last_outcome": "",
                        "outcome_type": "",
                        "last_update": time.time(),
                        "started": False,
                        "messages": []
                    }
                    st.session_state.my_name = my_name
                    st.session_state.room_code = room_code
                    st.session_state.is_creator = True
                    st.session_state.screen = "lobby"
                    st.session_state.local_last_update = rooms[room_code]["last_update"]
                    st.rerun()
                    
            if st.button("Cancel", key="cancel_host", use_container_width=True):
                st.session_state.online_action = ""
                st.rerun()
                
        elif st.session_state.online_action == "join":
            st.markdown("<p style='text-align:center; color:#cbd5e1; font-size:15px; margin-bottom:15px;'>Enter details to join your friend's room:</p>", unsafe_allow_html=True)
            my_name = st.text_input("Your Name", placeholder="Your name...", key="my_name_input_join").strip()
            join_code = st.text_input("Room Code", placeholder="e.g. 1234", key="join_code_input").strip()
            
            st.write("")
            if st.button("Join Room", use_container_width=True, type="primary"):
                if not my_name:
                    st.error("Please enter your name first!")
                elif not join_code:
                    st.error("Please enter the room code!")
                else:
                    rooms = get_rooms()
                    if join_code not in rooms:
                        st.error("Room not found! Please check the code.")
                    elif rooms[join_code]["started"]:
                        st.error("This game has already started!")
                    elif my_name in rooms[join_code]["players"]:
                        st.error("A player with this name is already in the room!")
                    else:
                        rooms[join_code]["players"].append(my_name)
                        rooms[join_code]["last_update"] = time.time()
                        st.session_state.my_name = my_name
                        st.session_state.room_code = join_code
                        st.session_state.is_creator = False
                        st.session_state.screen = "lobby"
                        st.session_state.local_last_update = rooms[join_code]["last_update"]
                        st.rerun()
                        
            if st.button("Cancel", key="cancel_join", use_container_width=True):
                st.session_state.online_action = ""
                st.rerun()

# ---------- SCREEN: GAME LOBBY ----------
elif st.session_state.screen == "lobby":
    set_bg("photos/second.png")
    st.markdown('<div class="title">Game Lobby</div>', unsafe_allow_html=True)
    st.write("")
    
    rooms = get_rooms()
    room_code = st.session_state.room_code
    
    if room_code not in rooms:
        st.error("Room disconnected or closed.")
        if st.button("Back to Home", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()
    else:
        room = rooms[room_code]
        
        st.markdown(f"""
        <div class="center" style="
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid rgba(0, 212, 255, 0.25);
            box-shadow: 0 0 25px rgba(0, 212, 255, 0.15);
        ">
            <h2 style='color:#ffd200; font-family:"Rajdhani", sans-serif; font-size:20px; margin-top:0;'>Room Code</h2>
            <span style='color:#00d4ff; font-family:"Rajdhani", sans-serif; font-size:48px; font-weight:800; letter-spacing:4px; text-shadow:0 0 15px rgba(0,212,255,0.4);'>{room_code}</span>
            <p style='color:#cbd5e1; font-size:15px; margin-top:10px; margin-bottom:0;'>Share this code with your friend to play online!</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=False):
            st.markdown("<h3 style='color:white; font-size:20px; margin-top:0; margin-bottom:15px; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px; font-family:\"Rajdhani\", sans-serif;'>👥 Joined Players</h3>", unsafe_allow_html=True)
            for p in room["players"]:
                is_host = "👑 Host" if p == room["players"][0] else "👤 Joined"
                
                if st.session_state.is_creator and p != room["players"][0]:
                    col_p, col_k = st.columns([5, 1])
                    with col_p:
                        st.markdown(f"""
                        <div class="player-row">
                            <span style='flex-grow:1; font-weight:600;'>{p}</span>
                            <span style='font-size:12px; background:rgba(255,255,255,0.1); padding:4px 10px; border-radius:10px; color:#cbd5e1;'>{is_host}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_k:
                        st.markdown("<div style='margin-top:2px;'>", unsafe_allow_html=True)
                        if st.button("❌", key=f"kick_{p}", help=f"Kick {p}"):
                            room["players"].remove(p)
                            room["last_update"] = time.time()
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="player-row">
                        <span style='flex-grow:1; font-weight:600;'>{p}</span>
                        <span style='font-size:12px; background:rgba(255,255,255,0.1); padding:4px 10px; border-radius:10px; color:#cbd5e1;'>{is_host}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.write("")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.is_creator:
                    if st.button("🚀 Start Game", use_container_width=True, type="primary"):
                        if len(room["players"]) < 1:
                            st.error("Need at least 1 player to start!")
                        else:
                            room["started"] = True
                            room["current"] = random.choice(room["players"])
                            room["last_update"] = time.time()
                            st.session_state.screen = "game"
                            st.session_state.local_last_update = room["last_update"]
                            st.rerun()
                else:
                    st.info("Waiting for the host to start the game...")
                    
            with col2:
                if st.button("🚪 Leave Room", use_container_width=True):
                    if st.session_state.my_name in room["players"]:
                        room["players"].remove(st.session_state.my_name)
                    if len(room["players"]) == 0 or st.session_state.is_creator:
                        if room_code in rooms:
                            del rooms[room_code]
                    else:
                        room["last_update"] = time.time()
                    
                    st.session_state.screen = "home"
                    st.session_state.room_code = ""
                    st.session_state.my_name = ""
                    st.session_state.is_creator = False
                    st.rerun()

        @st.fragment(run_every=1.0)
        def lobby_sync_listener():
            r = get_rooms().get(room_code)
            if r:
                if st.session_state.my_name not in r["players"]:
                    st.session_state.screen = "home"
                    st.session_state.room_code = ""
                    st.session_state.my_name = ""
                    st.session_state.is_creator = False
                    st.rerun()
                elif r["started"]:
                    st.session_state.screen = "game"
                    st.session_state.local_last_update = r["last_update"]
                    st.rerun()
                elif r["last_update"] > st.session_state.local_last_update:
                    st.session_state.local_last_update = r["last_update"]
                    st.rerun()
            else:
                st.session_state.screen = "home"
                st.rerun()
                
        lobby_sync_listener()

# ---------- SCREEN 2 (OFFLINE SETUP) ----------
elif st.session_state.screen == "players":
    set_bg("photos/second.png")
    st.markdown('<div class="title">Add Players</div>', unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=False):
            st.markdown("""
            <div class="center" style="
                font-size:16px;
                font-weight:600;
                color: #cbd5e1;
                margin-bottom:15px;
            ">
                Enter player name to join local game
            </div>
            """, unsafe_allow_html=True)

            def add_player():
                name = st.session_state.get("player_input", "").strip()
                if name and name not in st.session_state.players:
                    st.session_state.players.append(name)
                    st.session_state.player_input = ""
                elif name in st.session_state.players:
                    st.warning(f"'{name}' is already added!")

            st.text_input("Player Name", placeholder="Type name here...", key="player_input", on_change=add_player, label_visibility="collapsed")

            if st.button("Add", use_container_width=True, type="primary"):
                add_player()
                st.rerun()

            if st.session_state.players:
                st.write("")
                st.markdown("<h4 style='color:white; font-size:14px; margin-bottom:8px; font-family:\"Rajdhani\", sans-serif;'>👥 Added Players:</h4>", unsafe_allow_html=True)
                for i, p in enumerate(st.session_state.players):
                    col_p, col_r = st.columns([5, 1])
                    with col_p:
                        st.markdown(f"<div class='player-row'><span style='flex-grow:1; font-weight:600;'>{p}</span><span style='font-size:12px; color:#cbd5e1;'>Player {i+1}</span></div>", unsafe_allow_html=True)
                    with col_r:
                        st.markdown("<div style='margin-top:2px;'>", unsafe_allow_html=True)
                        if st.button("❌", key=f"remove_{i}_{p}", help=f"Remove {p}", use_container_width=True):
                            st.session_state.players.pop(i)
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
            
            st.write("")
            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Start Game", use_container_width=True, type="primary"):
                    if len(st.session_state.players) > 0:
                        st.session_state.current = random.choice(st.session_state.players)
                        st.session_state.screen = "game"
                        st.rerun()
            with col2:
                if st.button("Skip", use_container_width=True):
                    st.session_state.players = ["Player 1", "Player 2"]
                    st.session_state.current = random.choice(st.session_state.players)
                    st.session_state.screen = "game"
                    st.rerun()

            st.write("")
            if st.button("🏠 Main Menu", use_container_width=True, key="back_to_menu_offline"):
                st.session_state.screen = "home"
                st.session_state.players = []
                st.session_state.current = ""
                st.session_state.bottle_angle = 0
                if "last_outcome" in st.session_state:
                    del st.session_state.last_outcome
                st.rerun()

# ---------- SCREEN 3 (GAME SCREEN) ----------
elif st.session_state.screen == "game":
    set_bg("photos/three.png")

    is_online = (st.session_state.mode == "online")
    room = None
    if is_online:
        rooms = get_rooms()
        room_code = st.session_state.room_code
        if room_code not in rooms:
            st.error("Room disconnected!")
            if st.button("Back to Home", use_container_width=True):
                st.session_state.screen = "home"
                st.rerun()
            st.stop()
        room = rooms[room_code]
        players = room["players"]
        num_players = len(players)
        current_player = room["current"]
        bottle_angle = room["bottle_angle"]
        is_spinning = room["is_spinning"]
        category = room["category"]
    else:
        players = st.session_state.players
        num_players = len(players)
        current_player = st.session_state.current
        bottle_angle = st.session_state.bottle_angle
        is_spinning = st.session_state.is_spinning
        category = st.session_state.category

    CATEGORIES = [
        ("⭐ Popular",  "popular"),
        ("💥 Xtreme",   "xtreme"),
        ("💑 Couple",   "couple"),
        ("🌶️ Spicy",    "spicy"),
        ("🧒 Kids",     "kids"),
        ("💼 Office",   "office"),
    ]

    left_col, game_col = st.columns([1, 3])

    with left_col:
        with st.container(border=False):
            st.markdown("<div style='color:white; font-weight:bold; font-size:18px; margin-bottom:12px; text-align:center;'>🎮 Mode</div>", unsafe_allow_html=True)
            
            my_turn = (not is_online) or (st.session_state.my_name == current_player)
            
            for label, key in CATEGORIES:
                btn_disabled = is_online and (not my_turn)
                if st.button(label, key=f"cat_{key}", use_container_width=True, disabled=btn_disabled):
                    if is_online:
                        room["category"] = key
                        room["last_update"] = time.time()
                        st.session_state.local_last_update = room["last_update"]
                    else:
                        st.session_state.category = key
                    st.rerun()
                    
            selected_label = next((label for label, key in CATEGORIES if key == category), category.capitalize())
            st.markdown(
                f"""
                <div style='
                    text-align: center;
                    margin-top: 15px;
                    background: linear-gradient(135deg, #7f00ff, #ff007f);
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    padding: 8px 12px;
                    border-radius: 15px;
                    box-shadow: 0 4px 12px rgba(255,0,204,0.3);
                '>
                    Selected: {selected_label}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if is_online:
                st.write("")
                st.markdown("<div style='color:white; font-weight:bold; font-size:18px; margin-bottom:12px; text-align:center;'>💬 Chat</div>", unsafe_allow_html=True)
                
                chat_container = st.container(height=250)
                with chat_container:
                    for msg in room.get("messages", []):
                        if msg["sender"] == st.session_state.my_name:
                            st.markdown(f"<div style='text-align:right; margin-bottom:8px;'><span style='background:rgba(0, 212, 255, 0.25); color:white; padding:8px 14px; border-radius:16px 16px 0px 16px; font-size:14px; display:inline-block; max-width:85%; word-wrap:break-word; text-align:left; line-height:1.4; border:1px solid rgba(0,212,255,0.1);'>{msg['text']}</span></div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div style='text-align:left; margin-bottom:8px;'><span style='font-size:11px; color:#cbd5e1; margin-left:4px;'>{msg['sender']}</span><br><span style='background:rgba(255, 255, 255, 0.15); color:white; padding:8px 14px; border-radius:16px 16px 16px 0px; font-size:14px; display:inline-block; max-width:85%; word-wrap:break-word; line-height:1.4; border:1px solid rgba(255,255,255,0.05);'>{msg['text']}</span></div>", unsafe_allow_html=True)
                
                def send_message():
                    text = st.session_state.get("chat_input_val", "").strip()
                    if text:
                        if "messages" not in room:
                            room["messages"] = []
                        room["messages"].append({"sender": st.session_state.my_name, "text": text})
                        room["last_update"] = time.time()
                        st.session_state.chat_input_val = ""
                        st.session_state.local_last_update = room["last_update"]
                
                st.text_input("Type a message...", key="chat_input_val", on_change=send_message, placeholder="Say hi or use emojis... 😂", label_visibility="collapsed")

    with game_col:
        if is_online:
            st.markdown(f"""
            <div style='text-align: center; color: rgba(255,255,255,0.7); font-size: 14px; margin-bottom: 10px;'>
                🌐 Room Code: <b>{room_code}</b> | Playing as: <b>{st.session_state.my_name}</b>
            </div>
            """, unsafe_allow_html=True)

        with open("photos/bottle.png", "rb") as f:
            bottle_b64 = base64.b64encode(f.read()).decode()

        st.markdown(f"<h1 class='center' style='color: #00d4ff; font-family:\"Rajdhani\", sans-serif; font-size:45px;'>Spin the Bottle</h1>", unsafe_allow_html=True)

        def spin_bottle():
            winner_idx = random.randint(0, num_players - 1)
            angle_per_player = (360 / num_players)
            target_player_angle = (winner_idx * angle_per_player)
            
            if is_online:
                room["winner_index"] = winner_idx
                room["bottle_angle"] += 1080 + target_player_angle - (room["bottle_angle"] % 360)
                room["current"] = players[winner_idx]
                room["is_spinning"] = True
                room["last_outcome"] = ""
                room["outcome_type"] = ""
                room["last_update"] = time.time()
                st.session_state.local_last_update = room["last_update"]
            else:
                st.session_state.winner_index = winner_idx
                st.session_state.bottle_angle += 1080 + target_player_angle - (st.session_state.bottle_angle % 360)
                st.session_state.current = players[winner_idx]
                st.session_state.is_spinning = True
                if "last_outcome" in st.session_state: del st.session_state.last_outcome
            st.rerun()

        player_html = ""
        for i, name in enumerate(players):
            angle_deg = i * (360 / num_players)
            angle_rad = math.radians(angle_deg - 90)
            color = "white"
            if not is_spinning and current_player == name:
                color = "#ffd200"
            lp = 50 + (42 * math.cos(angle_rad))
            tp = 50 + (42 * math.sin(angle_rad))
            player_html += f'<div style="position: absolute; left: {lp}%; top: {tp}%; transform: translate(-50%, -50%); color: {color}; font-weight: bold; font-size: 20px; text-shadow: 2px 2px 4px black; white-space: nowrap; font-family:\'Rajdhani\', sans-serif;">{name}</div>'

        st.markdown(f"""
        <style>
        .game-container {{
            position: relative;
            height: 400px;
            width: 100%;
            margin-top: 15px;
            margin-bottom: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgba(15,23,42,0.4);
            border-radius: 50%;
            max-width: 400px;
            margin-left: auto;
            margin-right: auto;
            border: 2px solid rgba(255,255,255,0.08);
            box-shadow: inset 0 0 30px rgba(0,0,0,0.5);
        }}
        .bottle-img {{
            width: 200px;
            height: 300px;
            object-fit: contain;
            transition: transform 3s cubic-bezier(0.25, 0.1, 0.25, 1);
            z-index: 10;
            filter: drop-shadow(0 0 12px rgba(0,212,255,0.3));
        }}
        </style>
        <div class="game-container">
            <img src="data:image/png;base64,{bottle_b64}" class="bottle-img" style="transform: rotate({bottle_angle}deg);">
            {player_html}
        </div>
        """, unsafe_allow_html=True)

        col_l, col_c, col_r = st.columns([1.5, 2, 1.5])
        with col_c:
            if is_spinning:
                btn_text = "🌀 Spinning..."
                spin_disabled = True
            else:
                spin_disabled = is_online and (st.session_state.my_name != current_player)
                btn_text = "🍾 Spin!"
                if is_online and spin_disabled:
                    btn_text = f"⏳ {current_player}'s turn"
            if st.button(btn_text, key="spin_btn", use_container_width=True, disabled=spin_disabled, type="primary"):
                spin_bottle()

        if is_spinning:
            st.audio("assets/sound.wav", autoplay=True)
            time.sleep(3)
            if is_online:
                if st.session_state.my_name == current_player or st.session_state.is_creator:
                    room["is_spinning"] = False
                    room["last_update"] = time.time()
                    st.session_state.local_last_update = room["last_update"]
            else:
                st.session_state.is_spinning = False
            st.rerun()

        st.write("")

        col1, col2 = st.columns([1, 1])
        my_turn = (not is_online) or (st.session_state.my_name == current_player)
        
        with col1:
            if current_player and not is_spinning:
                if st.button("📖 Truth", use_container_width=True, disabled=(is_online and not my_turn)):
                    if is_online:
                        room["last_outcome"] = f"**{current_player}:** {get_truth(category, online=True)}"
                        room["outcome_type"] = "success"
                        room["last_update"] = time.time()
                        st.session_state.local_last_update = room["last_update"]
                    else:
                        st.session_state.last_outcome = f"**{current_player}:** {get_truth(st.session_state.category, online=False)}"
                        st.session_state.outcome_type = "success"
                    st.rerun()

        with col2:
            if current_player and not is_spinning:
                if st.button("🔥 Dare", use_container_width=True, disabled=(is_online and not my_turn)):
                    if is_online:
                        room["last_outcome"] = f"**{current_player}:** {get_dare(category, online=True)}"
                        room["outcome_type"] = "warning"
                        room["last_update"] = time.time()
                        st.session_state.local_last_update = room["last_update"]
                    else:
                        st.session_state.last_outcome = f"**{current_player}:** {get_dare(st.session_state.category, online=False)}"
                        st.session_state.outcome_type = "warning"
                    st.rerun()

        # Display Outcome Card
        if is_online:
            last_outcome = room.get("last_outcome", "")
            outcome_type = room.get("outcome_type", "")
        else:
            last_outcome = st.session_state.get("last_outcome", "")
            outcome_type = st.session_state.get("outcome_type", "")

        if last_outcome:
            st.write("")
            border_color = "rgba(0, 242, 254, 0.4)" if outcome_type == "success" else "rgba(255, 8, 68, 0.4)"
            title_text = "📖 Truth Unfolded" if outcome_type == "success" else "🔥 Dare Accepted"
            st.markdown(f"""
            <div style='
                background: rgba(15, 23, 42, 0.7);
                backdrop-filter: blur(12px);
                border: 1.5px solid {border_color};
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.5);
                color: white;
                margin-top: 10px;
                animation: slideUp 0.4s ease;
            '>
                <h4 style='margin-top:0; margin-bottom:8px; color:{'#00f2fe' if outcome_type == 'success' else '#ff0844'}; font-family:\"Rajdhani\", sans-serif; font-size:18px;'>{title_text}</h4>
                <p style='font-size:16px; margin:0; line-height:1.5;'>{last_outcome}</p>
            </div>
            <style>
            @keyframes slideUp {{
                0% {{ opacity: 0; transform: translateY(15px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}
            </style>
            """, unsafe_allow_html=True)

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Main Menu", use_container_width=True):
                if is_online:
                    if st.session_state.my_name in room["players"]:
                        room["players"].remove(st.session_state.my_name)
                    if len(room["players"]) == 0 or st.session_state.is_creator:
                        if room_code in rooms:
                            del rooms[room_code]
                    else:
                        room["last_update"] = time.time()
                    st.session_state.room_code = ""
                    st.session_state.my_name = ""
                    st.session_state.is_creator = False
                
                st.session_state.screen = "home"
                st.session_state.players = []
                st.session_state.current = ""
                st.session_state.bottle_angle = 0
                if "last_outcome" in st.session_state: del st.session_state.last_outcome
                st.rerun()

        with col2:
            reset_disabled = is_online and (not st.session_state.is_creator)
            if st.button("🔄 Reset Game", use_container_width=True, disabled=reset_disabled):
                if is_online:
                    room["current"] = random.choice(room["players"])
                    room["bottle_angle"] = 0
                    room["last_outcome"] = ""
                    room["outcome_type"] = ""
                    room["is_spinning"] = False
                    room["last_update"] = time.time()
                    st.session_state.local_last_update = room["last_update"]
                else:
                    st.session_state.current = random.choice(st.session_state.players)
                    st.session_state.bottle_angle = 0
                    if "last_outcome" in st.session_state: del st.session_state.last_outcome
                st.rerun()

        # Active listener for game updates
        if is_online:
            @st.fragment(run_every=1.0)
            def game_sync_listener():
                r = get_rooms().get(room_code)
                if r:
                    if st.session_state.my_name not in r["players"]:
                        st.session_state.screen = "home"
                        st.session_state.room_code = ""
                        st.session_state.my_name = ""
                        st.session_state.is_creator = False
                        st.rerun()
                    elif r["last_update"] > st.session_state.local_last_update:
                        st.session_state.local_last_update = r["last_update"]
                        st.rerun()
                else:
                    st.session_state.screen = "home"
                    st.rerun()
            game_sync_listener()