# Investment Tracker

This is a personal, self-directed project of mine that projects the growth of a users investments over time.
Built in Python and Streamlit, this investment tracker projects the growth of multiple accounts
dynamically through phase-based contribution and user input

## About

This project was built from scratch by me as my first project with Python from June 11th-21st of 2026
This project helped develop my Python skills while creating a tool I will actually use in the future.
Starting from almost zero knowledge of Python coding, I built out a simulator in a VS Code before 
converting to a Streamlit application.

## Features

- Projects growth between three accounts: Roth IRA, Brokerage, and Retirement/401(k)
- Phase-based Modeling: Users can create different contributions within timeframes to simulate real-life
changes in contribution (college, first job, main earning years)
- Models employee 401(k) matching 
- Warns users of IRS limits for Roth and 401(k) contribution limits
- Visual breakdown of account growth through a year-to-year table and graph with endpoint markers
- Target Overlay on graph to show when and if accounts pass a goal amount
- Accounts with no balance or contributions are automatically excluded from graphing
- Data exported to CSV file for further use
- Interactive sliders and inputs via Streamlit UI

## How to Run

**Requirements**
'''
pip3 install matplotlib streamlit pandas
'''
**Run Locally**
python3 -m streamlit run investment_tracker.py

## Build Log
- June 11th: Basic Growth Calculator, two-account table, inital graph| Line Count: 44
- June 12th: Dynamic endpoint annotation, grid, table formatting| Line Count: 48
- June 14th: Input validation, error messages, goal line, account exclusion outline| Line Count: 60
- June 15th: CSV export, rerun loop, goal value input| Line Count: 85
- June 17th: Phase-Based contributions and input, Roth limit warning, debugged rerun| Line Count: 119
- June 18th: 401(k) + employer match, retirement account limit warnings, converted UTMA to Brokerage Account| Line Count: 158
- June 20th: Streamlit setup, renamed file, initial UI conversion| Line Count: 159
- June 21st: Full conversion to Streamlit UI, stress testing, finalization, and GitHub publish| Line Count: 139

## What I Learned:

- Fundemental Python ideas: strings, lists, functions, dictionaries, f-strings, loops, etc
- Matplotlib data visualization
- Implementation of financial equations
- Input validation and error resolution
- Streamlit UI production
- Git and GitHub version control

## Next Up

- Public deployment through Streamlit Cloud
- Additional account types
- Enhanced UI

