import streamlit as st
import random
import numpy as np
import pandas as pd

# Set up the Streamlit app
st.title("Bingo Game")

# Create a session state to store drawn numbers
if 'drawn_numbers' not in st.session_state:
    st.session_state.drawn_numbers = []

# Function to draw a number
def draw_number():
    if len(st.session_state.drawn_numbers) < 100:
        while True:
            num = random.randint(1, 100)
            if num not in st.session_state.drawn_numbers:
                st.session_state.drawn_numbers.append(num)
                break

# Button to draw a number
if st.button("Draw Number"):
    draw_number()

# Reset button to clear drawn numbers
if st.button("Reset Game"):
    st.session_state.drawn_numbers = []

# Display drawn numbers in a 10x10 grid
st.header("Bingo Board:")
grid_size = 10
# Create a grid filled with placeholders
grid = np.full((grid_size, grid_size), '', dtype=object)

# Fill the grid with drawn numbers
for num in st.session_state.drawn_numbers:
    if num <= 100:  # Only consider numbers from 1 to 100
        row, col = divmod(num - 1, grid_size)
        grid[row, col] = num

# Create a DataFrame from the grid for better display
df_grid = pd.DataFrame(grid)

# Display the DataFrame in a styled table with increased font size
st.table(df_grid.style.set_properties(**{'font-size': '24px', 'text-align': 'center'}))
