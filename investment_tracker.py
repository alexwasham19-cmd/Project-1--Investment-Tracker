# Welcome too my first ever coding project! This is a basic investment projector
import streamlit as st
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import csv
import pandas as pd
# While coded with Python, this program is run through Streamlit. The following section prints the page title and inputs in a sidebar.
st.title("Investment Tracker")
with st.sidebar:
    x = st.text_input('Enter your name: ', key='name')
    B_balance = st.number_input('Enter your initial Brokerage balance: ', min_value=0.0, step=1000.0, key= 'B_balance')
    Roth_balance = st.number_input('Enter your initial Roth IRA balance: ', min_value=0.0, step=1000.0, key= 'Roth_balance')
    years = int(st.slider('Enter the number of years: ', min_value=1, max_value=50, step=1, key= 'years'))
    num_phases = int(st.slider('Enter the number of phases: ', min_value=1, max_value=5, step=1, key= 'num_phases'))
balance_401k = 0
phases = []
# The following section divdes the user's timeframe into phases, which reflect changing circumstances of life, dynamic contribution was a key feature I wanted to add.
with st.sidebar:
    for i in range(num_phases):
        st.write(f'Phase {i + 1}:')
        duration = st.slider(' Duration (years): ', min_value=1, max_value=50, step=1, key=f'duration_{i}')
        roth = st.number_input(' Monthly Roth Contribution: ', min_value=0.0, step=100.0, key=f'roth_{i}')
        if roth * 12 > 7000:
            st.warning('Warning: Your monthly Roth contribution exceeds the annual limit of $7,000.')
        elif roth * 12 == 7000:
            st.info('Note: Your monthly Roth contribution equals the annual limit of $7,000.')
        brokerage = st.number_input(' Monthly Brokerage Contribution: ', min_value=0.0, step=100.0, key=f'brokerage_{i}')
        retirement = st.number_input(' Monthly Retirement Contribution: ', min_value=0.0, step=100.0, key=f'retirement_{i}')
        if retirement * 12 > 24500:
            st.warning('Warning: Your monthly retirement contribution exceeds the annual limit of $24,500.')
        elif retirement * 12 == 24500:
            st.info('Note: Your monthly retirement contribution equals the annual limit of $24,500.')
        match = st.number_input(' Monthly 401(k) Match: ', min_value=0.0, step=100.0, key=f'match_{i}')
        if match + retirement > 72000:
            st.warning('Warning: Your total monthly retirement contribution and match exceeds the annual limit of $72,000.')
        phases.append({'duration': duration, 'roth': roth, 'brokerage': brokerage, 'retirement': retirement, 'match': match})
    rr_annual = st.slider('Enter the annual return rate (%): ', min_value=0.0, max_value=15.0, step=0.1, key='rr_annual') / 100
    total_goal = st.number_input('Enter your total goal amount: ', min_value=0.0, step=1000.0, key='total_goal')
# After inputing contributions, time, and phases, the user hits the big button to see their future.
# This loop calculates account balances through running totals which are saved and updated each simulated year.
if st.button('Calculate'):
    year_contributions = []
    for phase in phases:
        for year in range(phase['duration']):
            year_contributions.append({'roth': phase['roth'], 'brokerage': phase['brokerage'], 'retirement': phase['retirement'], 'match': phase['match']})
    if len(year_contributions) != years:
        st.error(f'Error: Phase durations sum to {len(year_contributions)} years, but you entered {years} years. ')
        st.stop()
    st.write('Hello ' + x + ', welcome to your investment tracker')
    st.write('This tracker shows the ' + str(years) + ' year growth of your Roth IRA and Brokerage accounts')
    st.write('Use the variable tools to change the length of investments, monthly contribution, and annual return')
    Roth_Year_Total = []
    Brokerage_Year_Total = []
    Total_Year_Total = []
    initial_investment = B_balance + Roth_balance 
    total_gain = [0]
    Total_Invested_List = []
    running_investment = initial_investment
    k401_Total = []
    # The 'for year' loop calculates the exact values of every account each month and updates each account list yearly.
    for year in range(1, years + 1):
        current = year_contributions[year - 1]
        mr_contributions = current['roth']
        mu_contribution = current['brokerage']
        retirement_contribution = current['retirement'] + current['match']
        running_investment += (mr_contributions + mu_contribution + retirement_contribution) * 12
        Total_Invested = f'${running_investment:,.2f}'
        Total_Invested_List.append(running_investment)
        for month in range(12):
            B_balance += mu_contribution
            B_balance *= (1 + rr_annual / 12)
            Roth_balance += mr_contributions
            Roth_balance *= (1 + rr_annual / 12)
            roth_str = f'${Roth_balance:,.2f}'
            brokerage_str = f'${B_balance:,.2f}'
            balance_401k += retirement_contribution
            balance_401k *= (1 + rr_annual / 12)
            k401_str = f'${balance_401k:,.2f}'
            total_str = f'${Roth_balance + B_balance + balance_401k:,.2f}'
        k401_Total.append(balance_401k)
        total_gain.append((Roth_balance + B_balance + balance_401k) - initial_investment)
        Roth_Year_Total.append(Roth_balance)
        Brokerage_Year_Total.append(B_balance)
        Total_Year_Total.append(Roth_balance + B_balance + balance_401k)
    # Pandas saves the values of accounts year to year which is used for a number of different purposes later in the program including a save file, value table, and graph.
    df = pd.DataFrame({
        'Year': range(1, years + 1),
        'Roth IRA Balance': Roth_Year_Total,
        'Brokerage Balance': Brokerage_Year_Total,
        '401(k) Balance': k401_Total,
        'Total' : Total_Year_Total,
        'Amount Invested': Total_Invested_List
    })
    st.dataframe(df.style.format({
        'Roth IRA Balance': '${:,.2f}',
        'Brokerage Balance': '${:,.2f}',
        '401(k) Balance': '${:,.2f}',
        'Total': '${:,.2f}',
        'Amount Invested': '${:,.2f}'
    }))
    # Accounts Summary Sentence
    st.info(f'In {years} years, your total balance will be ${Roth_balance + B_balance + balance_401k:,.2f} with a total gain of ${total_gain[-1]:,.2f} on an investment of ${running_investment:,.2f}')
    # Using the saved data from earlier a graph is created to show account growth, however specific accounts will only be shown if there is an initial or contributed amount.
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    if Roth_balance > 0 or mr_contributions > 0: 
        plt.plot(range(1, years + 1), Roth_Year_Total, label='Roth IRA')
        plt.plot(years, Roth_Year_Total[-1],marker = 'o', linestyle='none')
        plt.annotate(f'${Roth_Year_Total[-1]:,.2f}', (years, Roth_Year_Total[-1]), textcoords='offset points', xytext=(0,10))
    if B_balance > 0 or mu_contribution > 0: 
        plt.plot(range(1, years + 1), Brokerage_Year_Total, label='Brokerage')
        plt.plot(years, Brokerage_Year_Total[-1],marker = 'o', linestyle='none')
        plt.annotate(f'${Brokerage_Year_Total[-1]:,.2f}', (years, Brokerage_Year_Total[-1]), textcoords='offset points', xytext=(0,25))
    if balance_401k > 0 or retirement_contribution > 0:
        plt.plot(range(1, years + 1), k401_Total, label='401(k)')
        plt.plot(years, k401_Total[-1],marker = 'o', linestyle='none')
        plt.annotate(f'${k401_Total[-1]:,.2f}', (years, k401_Total[-1]), textcoords='offset points', xytext=(0,40))
    headers = ['Year', 'Roth IRA Balance', 'Brokerage Balance', '401(k) Balance', 'Total Balance', 'Total Invested']
    # The following line creates a "zipped" file that can be exported into a tool like Excel or Sheets for further use.
    data = list(zip(range(1, years + 1), Roth_Year_Total, Brokerage_Year_Total, k401_Total, Total_Year_Total, Total_Invested_List))
    csv_data = df.to_csv(index=False)
    st.download_button(
        label='Download CSV',
        data=csv_data,
        file_name='investment_data.csv",
        mime='text/csv'
    )
    st.success('CSV file "investment_data.csv" has been created with the investment data.')
    plt.plot(range(1, years + 1), Total_Year_Total, label='Total')
    plt.plot(years, Total_Year_Total[-1],marker = 'o', linestyle='none')
    plt.annotate(f'${Total_Year_Total[-1]:,.2f}', (years, Total_Year_Total[-1]), textcoords='offset points', xytext=(0,40))
    plt.xlabel('Years')
    plt.ylabel('Balances ($)')
    plt.title('Investment Growth Over Time')
    plt.grid()
    if total_goal > 0:
        plt.axhline(total_goal, color='red', linestyle='--', label='Total Goal') 
    plt.legend()
    # The final line, it combines all the previous data and information into a multi-value graph for the user which can be saved, it is a physical projection of financial goals, achievement, and ambition.
    st.pyplot(fig)
