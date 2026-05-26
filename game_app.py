import streamlit as st
import pandas as pd
import math

# -------------------------
# 🎨 STYLE
# -------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f172a;
        color: white;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        text-align: center;
        color: white;
    }
    th, td {
        border: 1px solid #444;
        padding: 12px;
        text-align: center;
        vertical-align: middle;
    }
    th {
        background-color: #1f2937;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# 🃏 TITLE
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

if "game_over" not in st.session_state:
    st.session_state.game_over = False

# -------------------------
# RESET GAME
# -------------------------
def reset_game():
    st.session_state.initialized = False
    st.session_state.scores = {}
    st.session_state.wins = {}
    st.session_state.history = []
    st.session_state.round = 1
    st.session_state.game_over = False

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
# GAME OVER SCREEN
# -------------------------
elif st.session_state.round > 9 or st.session_state.game_over:

    st.markdown("## 🏁 Game Finished!")

    scores = st.session_state.scores

    # ranking
    ranking = sorted(scores.items(), key=lambda x: x[1])

    st.markdown("### 🏆 Final Ranking")

    for i, (player, score) in enumerate(ranking, start=1):
        medal = ""
        if i == 1:
            medal = "🥇"
        elif i == 2:
            medal = "🥈"
        elif i == 3:
            medal = "🥉"

        st.write(f"{medal} {i}. {player} → {score}")

    st.success(f"🏆 Winner: {ranking[0][0]}")

    st.button("🔄 Restart Game", on_click=reset_game)

# -------------------------
# MAIN GAME
# -------------------------
else:

    players = st.session_state.players

    st.markdown(f"### 🎯 Round {st.session_state.round}/9")

    winner = st.selectbox("🏆 Select Winner", players)
    round_type = st.selectbox("🎴 Round Type", [100, 150, 200])

    values = {}

    st.write("Enter scores for other players:")

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

        # others
        for p in players:
            if p != winner:
                val = values[p]

                if val == round_type:
                    st.session_state.scores[p] += val
                else:
                    st.session_state.scores[p] += val * multiplier

        # save history
        clean_scores = {
            p: int(math.ceil(v))
            for p, v in st.session_state.scores.items()
        }

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

    renamed = {}
    for p in st.session_state.players:
        renamed[p] = f"{p} ({st.session_state.wins[p]})"

    df.rename(columns=renamed, inplace=True)

    score_cols = [c for c in df.columns if c != "Round"]

    html = """
    <table>
        <tr>
    """

    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr>"

    for _, row in df.iterrows():

        scores = [row[c] for c in score_cols]
        min_score = min(scores)
        max_score = max(scores)

        html += "<tr>"

        for col in df.columns:

            val = row[col]

            if col == "Round":
                html += f"<td>{val}</td>"
            else:
                style = ""

                if val == min_score:
                    style = "background-color: lightgreen; font-weight: bold;"
                elif val == max_score:
                    style = "background-color: red; color: white;"

                html += f"<td style='{style}'>{val}</td>"

        html += "</tr>"

    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)
