# app.py
import random
import string
import streamlit as st

st.set_page_config(page_title="Hangman", page_icon="🪢", layout="centered")

HANGMANPICS = [
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]

WORD_LIST = [
    "aardvark",
    "baboon",
    "camel",
    "jazz",
    "grass",
    "follow",
    "castle",
    "cloud",
]

MAX_WRONG = 6  # indices 0..6


# --------------------- Game Logic --------------------- #
def new_game():
    word = random.choice(WORD_LIST).lower()
    st.session_state.word = word
    st.session_state.revealed = ["_"] * len(word)
    st.session_state.guessed = set()
    st.session_state.wrong = 0
    st.session_state.status = "playing"  # 'playing' | 'won' | 'lost'
    st.session_state.feedback = "Good luck! Guess a letter."


def process_guess(letter: str):
    if st.session_state.status != "playing":
        return

    letter = letter.lower().strip()
    if len(letter) != 1 or letter not in string.ascii_lowercase:
        st.session_state.feedback = "Please enter a single letter (A–Z)."
        return

    if letter in st.session_state.guessed:
        st.session_state.feedback = f"You already tried '{letter}'."
        return

    st.session_state.guessed.add(letter)
    word = st.session_state.word

    if letter in word:
        # reveal all occurrences
        for i, ch in enumerate(word):
            if ch == letter:
                st.session_state.revealed[i] = letter
        if "_" not in st.session_state.revealed:
            st.session_state.status = "won"
            st.session_state.feedback = "🎉 YOU WIN! Press 'New game' to play again."
            st.balloons()
        else:
            st.session_state.feedback = f"Nice! '{letter}' is in the word."
    else:
        st.session_state.wrong += 1
        if st.session_state.wrong >= MAX_WRONG:
            st.session_state.status = "lost"
            st.session_state.feedback = (
                f"💀 GAME OVER. The word was '{word}'. Press 'New game' to try again."
            )
        else:
            remaining = MAX_WRONG - st.session_state.wrong
            st.session_state.feedback = (
                f"Nope, no '{letter}'. {remaining} wrong guess(es) left."
            )


# --------------------- Init --------------------- #
if "word" not in st.session_state:
    new_game()

# --------------------- UI --------------------- #
st.title("🪢 Hangman")

top_cols = st.columns([1, 1])
with top_cols[0]:
    st.subheader("Gallows")
    st.code(HANGMANPICS[st.session_state.wrong])

with top_cols[1]:
    st.subheader("Word")
    st.markdown(
        f"<div style='letter-spacing:0.35em;font-size:2rem;font-weight:600;'>{' '.join(st.session_state.revealed)}</div>",
        unsafe_allow_html=True,
    )
    st.write(f"Wrong guesses: **{st.session_state.wrong} / {MAX_WRONG}**")

    # Guessed letters
    guessed_sorted = sorted(st.session_state.guessed)
    if guessed_sorted:
        st.caption("Guessed letters: " + " ".join(guessed_sorted))
    else:
        st.caption("No guesses yet.")

# Feedback banner
status_color = {
    "playing": "info",
    "won": "success",
    "lost": "error",
}[st.session_state.status]
getattr(st, status_color)(st.session_state.feedback)

# Guess via text input
with st.form("guess_form", clear_on_submit=True):
    letter = st.text_input(
        "Type a letter and press Enter:",
        max_chars=1,
        help="Letters A–Z",
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("Guess")
    if submitted and st.session_state.status == "playing":
        process_guess(letter)

# On-screen keyboard
st.subheader("Keyboard")
kb_disabled = st.session_state.status != "playing"


def letter_btn_row(chars):
    cols = st.columns(len(chars))
    for c, col in zip(chars, cols):
        col.button(
            c,
            key=f"kb-{c}",
            disabled=kb_disabled or (c.lower() in st.session_state.guessed),
            use_container_width=True,
            on_click=process_guess,
            args=(c.lower(),),
        )


letter_btn_row(list("QWERTYUIOP"))
letter_btn_row(list("ASDFGHJKL"))
letter_btn_row(list("ZXCVBNM"))

st.divider()
btn_cols = st.columns([1, 1, 2])
with btn_cols[0]:
    if st.button("🔁 New game", use_container_width=True):
        new_game()
with btn_cols[1]:
    with st.expander("Word list (for instructors)", expanded=False):
        st.write(", ".join(WORD_LIST))
        st.caption("Edit WORD_LIST in the code to customize.")

# Footer / instructions
st.caption(
    "Rules: Guess the hidden word by trying letters. Wrong guesses build the hangman. "
    f"You lose after {MAX_WRONG} wrong guesses."
)
