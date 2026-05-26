import streamlit as st
import pandas as pd
import math

# -------------------------
# 🎨 GLOBAL STYLE
# -------------------------
st.markdown("""
<style>

.stApp {
    background-color: #1e293b;
    color: white;
}

/* scrollable tables on phone */
.table-container {
    overflow-x: auto;
    width: 100%;
    padding: 8px;
    border-radius: 12px;
}

/* ALL TABLES */
table {
    width: 100%;
    min-width: 650px;
    border-collapse: collapse;
    text-align: center;
    color: white;
    font-size: 14px;
    background-color: #0f172a;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

th {
    background-color: #111827;
    padding: 12px;
    border: 2px solid #94a3b8;
    text-align: center;
}

td {
    background-color: #1f2937;
    border: 2px solid #94a3b8;
    padding: 10px;
    text-align: center;
    vertical-align: middle;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# 🃏 TITLE
# -------------------------
st.markdown("""
<div style="
    background: linear-gradient(90deg, #111827, #1f2937);
    padding: 22px;
    border-radius: 15px;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 20px;
    color:white;
">
    🃏 14 Game Score Tracker 🃏
</div>
""", unsafe_allow_html=True)

# -------------------------
# SESSION STATE
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

    # -------------------------
    # GAME ACTIVE
    # -------------------------
    if not st.session_state.game_over:

        winner = st.selectbox("🏆 Select Winner", players)

        round_type = st.selectbox(
            "🎴 Round Type",
            [100, 150, 200]
        )

        values = {}

        st.write("Enter scores for other players:")

        for p in players:

            if p != winner:

                values[p] = st.number_input(
                    p,
                    min_value=0,
                    step=1
                )

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

            # save clean scores
            clean_scores = {}

            for p, v in st.session_state.scores.items():
                clean_scores[p] = int(math.ceil(float(v)))

            st.session_state.history.append({
                "Round": st.session_state.round,
                **clean_scores
            })

            st.session_state.round += 1

            # END GAME AFTER ROUND 9
            if st.session_state.round > 9:
                st.session_state.game_over = True

            st.rerun()

    # -------------------------
    # GAME OVER MESSAGE
    # -------------------------
    else:
        st.info("🏁 Game Finished — Final Ranking Below")

# -------------------------
# 📊 SCORE TABLE
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

    html = "<div class='table-container'>"
    html += "<table>"

    # header
    html += "<tr>"

    for col in df.columns:
        html += f"<th>{col}</th>"

    html += "</tr>"

    # rows
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

                # best score
                if val == min_score:
                    style = """
                    background-color:#22c55e;
                    font-weight:bold;
                    """

                # worst score
                elif val == max_score:
                    style = """
                    background-color:#ef4444;
                    color:white;
                    """

                html += f"<td style='{style}'>{val}</td>"

        html += "</tr>"

    html += "</table></div>"

    st.markdown(html, unsafe_allow_html=True)

# -------------------------
# 🏁 FINAL RANKING TABLE
# -------------------------
if st.session_state.game_over:

    st.markdown("---")

    st.markdown("""
    <div style="
        text-align:center;
        font-size:34px;
        font-weight:bold;
        margin-bottom:20px;
        color:white;
    ">
        🏁 GAME OVER 🏁
    </div>
    """, unsafe_allow_html=True)

    ranking = sorted(
        st.session_state.scores.items(),
        key=lambda x: x[1]
    )

    medals = ["🥇", "🥈", "🥉", "🎖️"]

    final_html = """
    <div class='table-container'>
    <table>
        <tr>
            <th>Rank</th>
            <th>Player</th>
            <th>Final Score</th>
        </tr>
    """

    for i, (player, score) in enumerate(ranking, start=1):

        if i == 1:
            bg = "#22c55e"

        elif i == 2:
            bg = "#3b82f6"

        elif i == 3:
            bg = "#eab308"

        else:
            bg = "#475569"

        final_html += f"""
        <tr style="background-color:{bg}; font-weight:bold;">

            <td style="
                border:2px solid #94a3b8;
                padding:12px;
                font-size:22px;
            ">
                {medals[i-1]} #{i}
            </td>

            <td style="
                border:2px solid #94a3b8;
                padding:12px;
            ">
                {player}
            </td>

            <td style="
                border:2px solid #94a3b8;
                padding:12px;
            ">
                {score}
            </td>

        </tr>
        """

    final_html += "</table></div>"

    st.markdown(final_html, unsafe_allow_html=True)

# -------------------------
# 🏆 LIVE LEADERBOARD
# -------------------------
if st.session_state.scores:

    best = min(
        st.session_state.scores,
        key=st.session_state.scores.get
    )

    worst = max(
        st.session_state.scores,
        key=st.session_state.scores.get
    )

    st.markdown("---")

    st.success(f"🏆 Leader: {best}")
    st.error(f"💀 Last Place: {worst}")
