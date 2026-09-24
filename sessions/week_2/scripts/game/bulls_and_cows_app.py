import streamlit as st

secret = "4271"

st.title("Bulls and Cows")
st.write("Guess the 4-digit number.")

if "past_guesses" not in st.session_state:
    st.session_state.past_guesses = []

guess = st.text_input("Your guess:")

if st.button("Submit"):

    if len(guess) != 4:
        st.write("Please enter exactly 4 digits.")

    else:

        bulls = 0
        cows = 0

        for i in range(4):

            if guess[i] == secret[i]:
                bulls = bulls + 1

            elif guess[i] in secret:
                cows = cows + 1

        st.write("Bulls:", bulls)
        st.write("Cows:", cows)

        st.session_state.past_guesses.append(guess)

        if bulls == 4:
            st.success("You win!")

st.write("Past guesses:")
st.write(st.session_state.past_guesses)
