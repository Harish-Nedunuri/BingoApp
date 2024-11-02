import streamlit as st
import random
import numpy as np
import pandas as pd
import os

# Set up the Streamlit app
st.title("Bingo Game")

# Add an image to the sidebar
st.sidebar.image("bingoapp.png", caption="Let's Play Bingo!", use_column_width=True)

# CSV file to store drawn numbers
csv_file = "drawn_numbers.csv"

# Load previously drawn numbers from the CSV file if it exists
if 'drawn_numbers' not in st.session_state:
    if os.path.exists(csv_file):
        # Read the CSV file, skipping the header row
        st.session_state.drawn_numbers = pd.read_csv(csv_file, skiprows=1, header=None, names=['number'])['number'].tolist()
        # Convert all loaded numbers to integers
        st.session_state.drawn_numbers = [int(num) for num in st.session_state.drawn_numbers if str(num).isdigit()]
    else:
        st.session_state.drawn_numbers = []

# Function to draw a number
def draw_number():
    if len(st.session_state.drawn_numbers) < 100:
        while True:
            num = random.randint(1, 100)
            if num not in st.session_state.drawn_numbers:
                st.session_state.drawn_numbers.append(num)
                
                # Append the drawn number to the CSV file, adding a header if the file does not exist
                with open(csv_file, 'a') as f:
                    if os.stat(csv_file).st_size == 0:
                        f.write("number\n")  # Write the header if file is empty
                    f.write(f"{num}\n")
                break

# Button to draw a number
if st.button("Draw Number"):
    draw_number()

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

# Convert all non-empty cells to integers for compatibility with Arrow
df_grid = pd.DataFrame(grid).applymap(lambda x: int(x) if isinstance(x, (int, float, str)) and str(x).isdigit() else x)

# Identify the latest drawn number
latest_number = st.session_state.drawn_numbers[-1] if st.session_state.drawn_numbers else None

# Function to highlight the latest drawn number in red
def highlight_latest(val):
    if val == latest_number:
        return 'color: red; font-weight: bold'
    return ''

# Display the DataFrame in a styled table with increased font size
st.table(df_grid.style.map(highlight_latest).set_properties(**{'font-size': '24px', 'text-align': 'center'}))

with st.sidebar:
    
    # Add a reset button with a confirmation prompt
    if 'confirm_reset' not in st.session_state:
        st.session_state.confirm_reset = False  # Initialize the reset confirmation flag

    if st.button("Reset Game"):
        st.session_state.confirm_reset = True  # Set the flag to show the confirmation prompt

    # If the reset flag is set, display the confirmation prompt
    if st.session_state.confirm_reset:
        st.warning("Are you sure you want to reset the game? This will clear all drawn numbers.")
        
        # Add Confirm and Cancel buttons in the confirmation prompt
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirm Reset"):
                # Perform the reset: clear drawn numbers and CSV file content
                st.session_state.drawn_numbers = []
                open(csv_file, 'w').close()  # Clear the CSV file
                st.session_state.confirm_reset = False  # Reset the confirmation flag
                st.success("The game has been reset.")
        with col2:
            if st.button("Cancel Reset"):
                # Cancel the reset by clearing the confirmation flag
                st.session_state.confirm_reset = False
                st.info("Reset canceled.")

