
import streamlit as st
import os
import base64
import random
import streamlit.components.v1 as components

st.set_page_config(
    page_title='Tic Tac Toe Pro',
    layout='centered'
)

# ---------------- CUSTOM CSS ----------------
st.markdown('''
<style>
.stApp {
    background-image: url("https://plus.unsplash.com/premium_photo-1675857197760-282b118999b9?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    min-height: 100vh;
    color: white;
}

.title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    color: white;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #e2e8f0;
    margin-bottom: 25px;
}

.status-box {
    padding: 14px;
    border-radius: 18px;
    text-align: center;
    font-size: 20px;
    font-weight: 700;
    color: white;
    background: rgba(0,0,0,0.45);
    backdrop-filter: blur(8px);
    margin-bottom: 20px;
}

.stButton > button {
    height: 90px;
    font-size: 34px;
    font-weight: 800;
    border-radius: 18px;
    border: none;
    background: rgba(0,0,0,0.35);
    color: white;
}
</style>
''', unsafe_allow_html=True)



# ---------------- SESSION ----------------
defaults = {
    'board': [['' for _ in range(3)] for _ in range(3)],
    'current_player': 'X',
    'winner': None,
    'game_over': False,
    'score_x': 0,
    'score_o': 0,
    'last_sound': None,
    'game_mode': 'Human vs Human'
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- SOUND ----------------
def play_sound(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            audio_bytes = f.read()

        b64 = base64.b64encode(audio_bytes).decode()

        components.html(
            f'''
            <audio autoplay style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            ''',
            height=0
        )


# ---------------- LOGIC ----------------
def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)):
        return True

    if all(board[i][2-i] == player for i in range(3)):
        return True

    return False


def is_draw(board):
    return all(cell != '' for row in board for cell in row)


def computer_move():
    empty_cells = []

    for i in range(3):
        for j in range(3):
            if st.session_state.board[i][j] == '':
                empty_cells.append((i, j))

    if empty_cells:
        row, col = random.choice(empty_cells)

        st.session_state.board[row][col] = 'O'

        if check_winner(st.session_state.board, 'O'):
            st.session_state.winner = 'O'
            st.session_state.game_over = True
            st.session_state.score_o += 1
            st.session_state.last_sound = "loss.mp3"

        elif is_draw(st.session_state.board):
            st.session_state.game_over = True
            st.session_state.last_sound = "draw.mp3"

        else:
            st.session_state.current_player = 'X'


def make_move(row, col):
    if st.session_state.game_over:
        return

    if st.session_state.board[row][col] != '':
        return

    player = st.session_state.current_player
    st.session_state.board[row][col] = player

    if check_winner(st.session_state.board, player):
        st.session_state.winner = player
        st.session_state.game_over = True

        if player == 'X':
            st.session_state.score_x += 1
            st.session_state.last_sound = "win.mp3"
        else:
            st.session_state.score_o += 1
            st.session_state.last_sound = "loss.mp3"

    elif is_draw(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.last_sound = "draw.mp3"

    else:
        if st.session_state.game_mode == "Human vs Computer":
            st.session_state.current_player = 'O'
            computer_move()
        else:
            st.session_state.current_player = 'O' if player == 'X' else 'X'


def reset_board():
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = 'X'
    st.session_state.winner = None
    st.session_state.game_over = False
    st.session_state.last_sound = None


# ---------------- UI ----------------
st.markdown('<div class="title">🎮 Tic Tac Toe Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Play with Friend or Computer 🤖</div>', unsafe_allow_html=True)

mode = st.selectbox(
    "🎯 Select Mode",
    ["Human vs Human", "Human vs Computer"]
)

st.session_state.game_mode = mode

col1, col2 = st.columns(2)

with col1:
    st.metric('Player X', st.session_state.score_x)

with col2:
    st.metric('Player O', st.session_state.score_o)

if st.session_state.winner:
    st.markdown(
        f'<div class="status-box">🏆 Player {st.session_state.winner} Wins!</div>',
        unsafe_allow_html=True
    )

elif st.session_state.game_over:
    st.markdown(
        '<div class="status-box">🤝 It is a Draw!</div>',
        unsafe_allow_html=True
    )

else:
    st.markdown(
        f'<div class="status-box">✨ Current Turn: {st.session_state.current_player}</div>',
        unsafe_allow_html=True
    )

if st.session_state.last_sound:
    play_sound(st.session_state.last_sound)
    st.session_state.last_sound = None

for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        value = st.session_state.board[i][j] or ' '
        if cols[j].button(value, key=f'{i}-{j}', use_container_width=True):
            make_move(i, j)
            st.rerun()

st.divider()
st.button('🔄 New Round', on_click=reset_board, use_container_width=True)
