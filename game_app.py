import streamlit as st
import pandas as pd
import math

st.title("14 Game Score Tracker")

# -------------------------
# INIT SESSION STATE
# -------------------------
if "initialized" not in st.session_state:
    st.session_state.initialized = False

if "scores" not in st.session_state:
    st.session_state.scores = {}

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

    # Winner + round type
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

        # winner penalty
        st.session_state.scores[winner] += penalty

        # other players logic
        for p in players:
            if p != winner:
                val = values[p]

                if val == round_type:
                    st.session_state.scores[p] += val
                else:
                    st.session_state.scores[p] += val * multiplier

        # -------------------------
        # SAVE HISTORY (CLEAN + CEIL)
        # -------------------------
        clean_scores = {}

        for p, v in st.session_state.scores.items():
            clean_scores[p] = int(math.ceil(float(v)))

        st.session_state.history.append(
            {
                "Round": st.session_state.round,
                **clean_scores
            }
        )

        st.session_state.round += 1

        st.rerun()

    # -------------------------
    # SCORE TABLE
    # -------------------------
    st.subheader("Score Table")

    if st.session_state.history:

        df = pd.DataFrame(st.session_state.history)

        # highlight lowest score (winner)
        def highlight(row):
            scores = row[1:]
            min_score = scores.min()
            return ["background-color: lightgreen" if v == min_score else "" for v in row]

        st.dataframe(df.style.apply(highlight, axis=1))

    # -------------------------
    # CURRENT WINNER
    # -------------------------
    if st.session_state.scores:

        current_winner = min(
            st.session_state.scores,
            key=st.session_state.scores.get
        )

        st.success(f"Current Leader: {current_winner}")