import streamlit as st
import pandas as pd
import math

# -------------------------
# 🎨 GLOBAL STYLE (DARK + CENTER FIX)
# -------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f172a;
        color: white;
    }

    table {
        text-align: center !important;
    }

    th {
        text-align: center !important;
    }

    td {
        text-align: center !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# 🃏 TITLE CARD
# -------------------------
st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, #111827, #1f2937);
        padding: 22px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 30px;
        font-weight: bold;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    ">
        🃏 14 Game Score Tracker 🃏
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# INIT STATE
# -------------------------
if "initialized" not in st.session_state:
    st.session_state.initialized = False

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "wins" not in st.session_state:
    st.session_state.wins = {}

if "history" not in st.session_state:
    st.session_state.history = []

if "round" not in st.session_state:
    st.session_state.round = 1

# -------------------------
# PLAYER SETUP
# -------------------------
if not st.session_state.initialized:

    st.subheader("🎮 Enter Player Names")

    p1 = st.text_input("Player 1")
    p2 = st.text_input("Player 2")
    p3 = st.text_input("Player 3")
    p4 = st.text_input("Player 4")

    if st.button("Start Game 🚀"):

        if p1 and p2 and p3 and p4:

            players = [p1, p2, p3, p4]

            st.session_state.players = players
            st.session_state.scores = {p: 0 for p in players}
            st.session_state.wins = {p: 0 for p in players}
            st.session_state.initialized = True

            st.rerun()

        else:
            st.warning("⚠️ Please enter all player names")

# -------------------------
# MAIN GAME
# -------------------------
else:

    players = st.session_state.players

    st.markdown("### 🎯 Round Control")

    winner = st.selectbox("🏆 Select Winner", players)
    round_type = st.selectbox("🎴 Round Type", [100, 150, 200])

    st.write("Enter scores for other players:")

    values = {}

    for p in players:
        if p != winner:
            values[p] = st.number_input(p, min_value=0, step=1)

    # -------------------------
    # APPLY ROUND
    # -------------------------
    if st.button("Apply Round ➕"):

        if round_type == 100:
            penalty = -20
            multiplier = 1
        elif round_type == 150:
            penalty = -30
            multiplier = 1.5
        else:
            penalty = -40
            multiplier = 2

        # winner logic
        st.session_state.scores[winner] += penalty
        st.session_state.scores[winner] -= 100
        st.session_state.wins[winner] += 1

        # other players
        for p in players:
            if p != winner:
                val = values[p]

                if val == round_type:
                    st.session_state.scores[p] += val
                else:
                    st.session_state.scores[p] += val * multiplier

        # save history (rounded up)
        clean_scores = {}

        for p, v in st.session_state.scores.items():
            clean_scores[p] = int(math.ceil(float(v)))

        st.session_state.history.append({
            "Round": st.session_state.round,
            **clean_scores
        })

        st.session_state.round += 1

        st.rerun()

# -------------------------
# TABLE DISPLAY
# -------------------------
st.markdown("---")
st.subheader("📊 Score Table")

if st.session_state.history:

    df = pd.DataFrame(st.session_state.history)

    # rename columns with wins
    renamed = {}
    for p in st.session_state.players:
        renamed[p] = f"{p} ({st.session_state.wins[p]})"

    df.rename(columns=renamed, inplace=True)

    # -------------------------
    # HIGHLIGHT FUNCTION
    # -------------------------
    def highlight(row):

        scores = [row[c] for c in row.index if c != "Round"]

        min_score = min(scores)
        max_score = max(scores)

        styles = []

        for col in row.index:

            if col == "Round":
                styles.append("text-align:center")

            else:
                val = row[col]

                if val == min_score:
                    styles.append("background-color: lightgreen; font-weight: bold; text-align:center")

                elif val == max_score:
                    styles.append("background-color: red; color: white; text-align:center")

                else:
                    styles.append("text-align:center")

        return styles

    st.dataframe(
        df.style.apply(highlight, axis=1).set_properties(**{
            "text-align": "center"
        })
    )

# -------------------------
# LEADERBOARD
# -------------------------
st.markdown("---")

if st.session_state.scores:

    best = min(st.session_state.scores, key=st.session_state.scores.get)
    worst = max(st.session_state.scores, key=st.session_state.scores.get)

    st.success(f"🏆 Leader: {best}")
    st.error(f"💀 Last Place: {worst}")
