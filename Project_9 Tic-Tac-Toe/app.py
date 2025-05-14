# --- Import Libraries ---
import streamlit as st
import random

# --- Page Configuration ---
st.set_page_config(page_title="Tic-Tac-Toe", layout="centered")
st.title("🎮 Tic-Tac-Toe (Single Player vs Computer)")
st.markdown("Play as ❌. Computer plays as ⭕")

# --- Initialize Game State ---
if 'board' not in st.session_state:
    st.session_state.board = [""] * 9  # 3x3 board initialized with empty strings
    st.session_state.winner = None  # No winner at the start

# --- Function to Check for Winner or Draw ---
def check_winner(board):
    win_conditions = [
        (0,1,2), (3,4,5), (6,7,8),  # Rows
        (0,3,6), (1,4,7), (2,5,8),  # Columns
        (0,4,8), (2,4,6)           # Diagonals
    ]
    for i, j, k in win_conditions:
        if board[i] == board[j] == board[k] and board[i] != "":
            return board[i]  # Return 'X' or 'O'
    if "" not in board:
        return "Draw"  # If no empty cells left
    return None

# --- Function for Computer's Move ---
def computer_move():
    empty_indices = [i for i, val in enumerate(st.session_state.board) if val == ""]
    if empty_indices:
        move = random.choice(empty_indices)  # Randomly pick one empty spot
        st.session_state.board[move] = "O"

# --- Function to Reset the Game ---
def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.winner = None

# --- Create Game Grid (3x3) ---
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        if st.session_state.board[i] == "" and not st.session_state.winner:
            if st.button(" ", key=i):
                st.session_state.board[i] = "X"  # Player move
                st.session_state.winner = check_winner(st.session_state.board)

                if not st.session_state.winner:
                    computer_move()  # Let computer play
                    st.session_state.winner = check_winner(st.session_state.board)

# --- Display Final Board State (as Disabled Buttons) ---
for i in range(9):
    with cols[i % 3]:
        if st.session_state.board[i] != "":
            st.button(st.session_state.board[i], key=f"static_{i}", disabled=True)

# --- Show Result Message ---
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.warning("🤝 It's a Draw!")
    elif st.session_state.winner == "X":
        st.success("🎉 You Win!")
    else:
        st.error("💻 Computer Wins!")

    # --- Restart Button ---
    st.button("🔁 Play Again", on_click=reset_game)

# --- Footer ---
st.markdown("""
---
<p style='text-align:center;'>Created with ❤️ by Nabia Haider</p>
""", unsafe_allow_html=True)
