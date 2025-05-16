# --- Import Libraries ---
import streamlit as st  # Streamlit app banane ke liye
import random  # Random number (computer ki move) ke liye

# --- Game Logic Class ---
class TicTacToe:
    def __init__(self):  # Jab game start ho
        self.board = ['' for _ in range(9)]  # 3x3 board banaya, sab khali hai
        self.current_winner = None  # Shuru mein koi winner nahi hota

    def make_move(self, square, letter):  # Move karne ka function
        if self.board[square] == '':  # Agar square khali hai
            self.board[square] = letter  # Usme X ya O daal do
            if self.check_winner(square, letter):  # Check karo jeet to nahi gayi
                self.current_winner = letter  # Agar jeet gaya to winner set kardo
            return True
        return False  # Agar move invalid ho to False return karo

    def available_moves(self):  # Jitne bhi khali boxes hain unki list return karo
        return [i for i, val in enumerate(self.board) if val == '']

    def is_full(self):  # Agar board full hai (draw ho gaya) to True return karo
        return '' not in self.board

    def check_winner(self, square, letter):  # Check karo koi jeeta to nahi
        row_ind = square // 3  # Row number nikalo
        row = self.board[row_ind*3 : (row_ind+1)*3]  # Us row ke 3 elements nikalo
        if all([spot == letter for spot in row]):  # Agar row mein sab X ya sab O hain
            return True

        col_ind = square % 3  # Column number nikalo
        col = [self.board[col_ind + i*3] for i in range(3)]  # Us column ke 3 elements
        if all([spot == letter for spot in col]):  # Agar column mein sab same hain
            return True

        # Diagonal check sirf tab hoga jab square even number ho
        if square % 2 == 0:
            diag1 = [self.board[i] for i in [0,4,8]]  # First diagonal
            diag2 = [self.board[i] for i in [2,4,6]]  # Second diagonal
            if all([spot == letter for spot in diag1]) or all([spot == letter for spot in diag2]):
                return True

        return False  # Agar koi bhi condition match nahi hui to False

# --- Initialize Session State ---
if 'game' not in st.session_state:  # Agar game pehli baar load ho rahi hai
    st.session_state.game = TicTacToe()  # Game ka object create karo
    st.session_state.turn = 'X'  # Pehli turn X ki hoti hai (player)
    st.session_state.winner = None  # Shuru mein koi winner nahi hota

game = st.session_state.game  # Game object ko local variable mein rakho

# --- Page Config ---
st.set_page_config(page_title="Tic-Tac-Toe", layout="centered")  # Page ka title aur layout set karo
st.title("🎮 Tic-Tac-Toe (Single Player vs Computer)")  # Title show karo
st.markdown("Play as ❌. Computer plays as ⭕")  # User instructions

# --- Game Grid Buttons (Player Move) ---
cols = st.columns(3)  # 3 columns banaye board ke liye
for i in range(9):  # 0 se 8 tak loop chalega (9 boxes)
    with cols[i % 3]:  # Har column mein ek button dikhayenge
        symbol = game.board[i]  # Current box ka symbol dekho
        if symbol == '' and st.session_state.turn == 'X' and not game.current_winner:
            # Agar box khali hai, player ki turn hai, aur koi winner nahi hai
            if st.button(" ", key=f"move_{i}"):  # Button show karo
                game.make_move(i, 'X')  # Player X ki move apply karo
                if game.current_winner:  # Agar X jeet gaya
                    st.session_state.winner = 'X'  # Winner set karo
                    st.session_state.turn = None  # Turn end karo
                elif game.is_full():  # Agar draw ho gaya
                    st.session_state.winner = 'Draw'
                    st.session_state.turn = None
                else:
                    st.session_state.turn = 'O'  # Warna ab computer ki turn
                st.rerun()  # Page ko refresh karo taake update ho jaye
        elif symbol != '':  # Agar box bhara hua hai
            st.button(symbol, key=f"filled_{i}", disabled=True)  # Us symbol ka disabled button dikhayein
        else:
            st.markdown("### ⬜")  # Agar box bhara nahi to empty square dikhayein

# --- Computer Move ---
if st.session_state.turn == 'O' and not game.current_winner:
    available = game.available_moves()  # Jitne boxes available hain
    if available:
        move = random.choice(available)  # Random box choose karo
        game.make_move(move, 'O')  # O ki move lagao
        if game.current_winner:  # Agar O jeet gaya
            st.session_state.winner = 'O'
            st.session_state.turn = None
        elif game.is_full():  # Agar draw ho gaya
            st.session_state.winner = 'Draw'
            st.session_state.turn = None
        else:
            st.session_state.turn = 'X'  # Warna ab X ki turn
    st.rerun()  # Page ko refresh karo

# --- Game Result Display ---
if st.session_state.winner:  # Agar koi winner ya draw hai
    if st.session_state.winner == 'Draw':
        st.warning("🤝 It's a Draw!")  # Draw ka message
    elif st.session_state.winner == 'X':
        st.success("🎉 You Win!")  # Player X jeet gaya
    else:
        st.error("💻 Computer Wins!")  # Computer O jeet gaya

# --- Restart Game Button ---
st.markdown("---")  # Line separator
if st.button("🔁 Play Again"):  # Play again ka button
    st.session_state.game = TicTacToe()  # New game object banao
    st.session_state.turn = 'X'  # X se start karo
    st.session_state.winner = None  # Winner reset karo
    st.rerun()  # Page reload

# --- Footer ---
st.markdown("""
---
<p style='text-align:center;'>Created with ❤️ by Nabia Haider</p>
""", unsafe_allow_html=True)  # Neeche footer show karo
