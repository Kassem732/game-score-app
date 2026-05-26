import streamlit as st
import pandas as pd
import math

st.title("14 Game Score Tracker")

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

    st.subheader("Enter Player Names")

    p1 = st.text_input("Player 1")
    p2 = st.text_input("Player 2")
    p3 = st.text_input("Player 3")
    p4 = st.text_input("Player 4")

    if st.button("Start Game"):

        if p1 and p2 and p3 and p4:

            players = [p1, p2, p3, p4]

            st.session_state.players = players
            st.session_state.scores = {p: 0 for p in players}
            st.session_state.wins = {p: 0 for p in players}
            st.session_state.initialized = True

            st.rerun()

        else:
            st.warning("Please enter all player names")

# -------------------------
# MAIN GAME
# -------------------------
else:

    players = st.session_state.players

    st.subheader(f"Round {st.session_state.round}")

    winner = st.selectbox("Select winner", players)
    round_type = st.selectbox("Round type", [100, 150, 200])

    st.write("Enter scores for the other players:")

    values = {}

    for p in players:
        if p != winner:
            values[p] = st.number_input(p, min_value=0, step=1)

    # -------------------------
    # APPLY ROUND
    # -------------------------
    if st.button("Apply Round"):

        # rules
        if round_type == 100:
            penalty = -20
            multiplier = 1
        elif round_type == 150:
            penalty = -30
            multiplier = 1.5
        else:
            penalty = -40
            multiplier = 2

        # winner rule (NEW)
        st.session_state.scores[winner] += penalty
        st.session_state.scores[winner] -= 100  # NEW RULE
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
            **clean_scores,
            **{p + " Wins": st.session_state.wins[p] for p in players}
        })

        st.session_state.round += 1

        st.rerun()

    # -------------------------
    # TABLE
    # -------------------------
    st.subheader("Score Table")

    if st.session_state.history:

        df = pd.DataFrame(st.session_state.history)

        # highlight WORST player (highest score = red)
        def highlight(row):
            scores = row[1:1+len(players)]
            max_score = scores.max()

            styles = []

            for i, col in enumerate(row.index):
                if col == "Round":
                    styles.append("")
                elif col.endswith("Wins"):
                    styles.append("")
                else:
                    if row[col] == max_score:
                        styles.append("background-color: red; color: white")
                    else:
                        styles.append("")

            return styles

        st.dataframe(df.style.apply(highlight, axis=1))

    # -------------------------
    # CURRENT WORST PLAYER
    # -------------------------
    if st.session_state.scores:

        worst = max(st.session_state.scores, key=st.session_state.scores.get)

        st.error(f"Worst Player (Highest Score): {worst}")
