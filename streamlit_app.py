import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Inject custom CSS for styling
st.markdown("""
    <style>
    /* App Background */
    .stApp {
        background-color: #FFFFFF; /* White background */
    }

    /* Titles and Text Colors */
    h1, h2, h3, h4, h5, h6 {
        color: #232F3E;  /* Dark text color */
    }
    
    label {
        color: #232F3E;  /* Dark text for labels */
        font-weight: bold;
    }

    /* Input Field Borders */
    input, select {
        border-color: #232F3E;
        border-width: 2px;
    }

    /* Button Style with Gradient */
    div.stButton > button {
        background: linear-gradient(0deg, #F8C13C 0%, #F6DD9C 100%); /* Gradient background */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.4rem 1.2rem;
        font-size: 1rem;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background: linear-gradient(0deg, #F6DD9C 0%, #F8C13C 100%); /* Invert gradient on hover */
        color: black;  /* Change text color on hover */
        transition: 0.3s;
    }

    /* Yellow Submit Button Style */
    .stForm > div > button {
        background-color: #F8C13C;  /* Yellow background for submit button */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.4rem 1.2rem;
        font-size: 1rem;
        font-weight: bold;
    }

    .stForm > div > button:hover {
        background-color: #FFB84D; /* Lighter yellow on hover */
        color: black; /* Change text color on hover */
        transition: 0.3s;
    }

    /* Additional styles for improved readability */
    .stForm > div > div {
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize the session state to store dynamic fields if it's not already present
if 'dynamic_fields' not in st.session_state:
    st.session_state.dynamic_fields = []

# Function to add a new dynamic field with two input keys (value1 and value2)
def add_dynamic_field(title):
    new_field = {
        'title': title,
        'input_key_value1': f"value1_{len(st.session_state.dynamic_fields)}",
        'input_key_value2': f"value2_{len(st.session_state.dynamic_fields)}"
    }
    st.session_state.dynamic_fields.append(new_field)

# Input to create new dynamic field
st.subheader("Add Goals")
custom_title = st.text_input("Enter Goal Name")

# Button to add new dynamic field
if st.button("Add Goal"):
    if custom_title:
        add_dynamic_field(custom_title)
    else:
        st.warning("Please provide both a title and a label for the dynamic field!")

# Title of the app
st.title("Retirement Planning Form")
# Main form layout with static inputs
with st.form("retirement_planning_form"):
    # Create two columns for the static input fields
    col1, col2 = st.columns(2)

    # First column (left side) - static fields
    with col1:
        current_age = st.number_input("Current Age", min_value=1, max_value=120, step=1)
        present_portfolio = st.number_input("Present Portfolio (₹)", min_value=1, step=1)
        inflation_rate = st.number_input("Annual Inflation Rate (%)", min_value=0.0, max_value=20.0, value=7.0) / 100
        expected_returns = st.number_input("Expected Annual Returns", min_value=0.0, max_value=100.0, value=15.0) / 100

    # Second column (right side) - static fields
    with col2:
        monthly_sip = st.number_input("Monthly SIP", min_value=0, step=1000, value=51000)
        monthly_swp = st.number_input("Monthly SWP", min_value=0, step=1000, value=50000)
        expenses = st.text_input("Expenses (e.g., {30:500000, 35:10000000})", "{35:5000000, 40:50000000}")
        retirement_age = st.number_input("Retirement Age", min_value=1, max_value=120, step=1)
        expectancy_life = st.number_input("Expectancy Life", min_value=retirement_age, max_value=100, value=80)

    # Dynamic fields based on session state
    st.subheader("Goals")
    dynamic_col1, dynamic_col2 = st.columns(2)  # Create two columns for dynamic fields
    
    # Loop through dynamic fields and display them in two columns
    for i, field in enumerate(st.session_state.dynamic_fields):
        with dynamic_col1 if i % 2 == 0 else dynamic_col2:
            st.write(f"**{field.get('title', 'Untitled')}**")
            value1 = st.number_input(f"Value 1", key=field['input_key_value1'])
            value2 = st.number_input(f"Value 2", key=field['input_key_value2'])

    # Submit button
    submit = st.form_submit_button("Submit")

# After submission, display the entered data
if submit:
    st.sidebar.title("Investment Calculator")
    monthly_sip = monthly_sip
    expected_returns = expected_returns
    inflation_rate = inflation_rate
    current_age = current_age
    retirement_age = retirement_age
    current_valuation = present_portfolio
    expenses = expenses
    monthly_swp = monthly_swp
    expectancy_life = expectancy_life

    st.success("Form Submitted Successfully!")
    st.write(f"**Current Age**: {current_age}")
    st.write(f"**Present Portfolio**: ₹{present_portfolio}")
    st.write(f"**Annual Inflation Rate**: {inflation_rate}")
    st.write(f"**Expected Annual Returns**: {expected_returns}")
    st.write(f"**Monthly SIP**: ₹{monthly_sip}")
    st.write(f"**Monthly SWP**: ₹{monthly_swp}")
    st.write(f"**Retirement Age**: {retirement_age}")
    st.write(f"**Expenses**: ₹{expenses}")
    st.write(f"**Expectancy Life**: {expectancy_life}")
    

    # Display dynamic field values
    for field in st.session_state.dynamic_fields:
        value1 = st.session_state.get(field['input_key_value1'], '')
        value2 = st.session_state.get(field['input_key_value2'], '')
        st.write(f"**{field['title']}**: Value 1 - {value1}, Value 2 - {value2}")

    # # Placeholder calculation logic for SIP and ROI
    # monthly_savings_needed = (expense_post_retirement - income) / (retirement_age - current_age) if retirement_age > current_age else 0
    # estimated_roi = 0.08  # Assuming 8% annual return on investment
    
    # # Create a DataFrame to show results as a table
    # results = pd.DataFrame({
    #     "Metric": ["SIP Amount (₹)", "Estimated ROI (%)"],
    #     "Value": [f"{monthly_savings_needed:,.2f}", f"{estimated_roi * 100:.2f}%"]
    # })

    # Convert the expenses input to a dictionary
    expenses_dict = eval(expenses)

    # Calculate the corpus for each year
    start_year = 2024  # Assuming the current year is 2024
    years = range(start_year, start_year + expectancy_life - current_age + 1)
    corpus = [current_valuation]
    sip_corpus = [0] * len(years)
    swp_corpus = [0] * len(years)
    invested_sum = 0
    withdrawn_sum = 0

    # Loop through each year and calculate corpus, SIP, SWP, and expenses
    for i, year in enumerate(years):
        age = current_age + (year - start_year)
        
        # Apply SIP if the user is below retirement age
        if age < retirement_age:
            # Monthly SIP with annual returns
            invested_sum += monthly_sip * 12 * (1 + inflation_rate)**(year - start_year)
            corpus[-1] *= (1 + expected_returns)  # Apply returns on existing corpus
            corpus[-1] += monthly_sip * 12 * (1 + inflation_rate)**(year - start_year)  # Add SIP
        else:
            # Monthly SWP if the user has retired
            withdrawn_sum += monthly_swp * 12 * (1 + inflation_rate)**(year - start_year)
            corpus[-1] *= (1 + expected_returns)  # Apply returns on existing corpus
            corpus[-1] -= monthly_swp * 12 * (1 + inflation_rate)**(year - start_year)  # Deduct SWP
            
        # Deduct any specified expenses for the year
        if age in expenses_dict:
            corpus[-1] -= expenses_dict[age] * (1 + inflation_rate)**(year - start_year)

        # Prevent corpus from going below zero
        corpus[-1] = max(corpus[-1], 0)
        
        # Add current values to the corpus list for the next iteration
        corpus.append(corpus[-1])
        sip_corpus[i] = invested_sum
        swp_corpus[i] = withdrawn_sum

    # Create the data frame for the chart
    data = pd.DataFrame({
        'Year': years,
        'Corpus': corpus[:-1],  # Last value is extra
        'Invested Sum': sip_corpus,
        'Withdrawn Sum': swp_corpus
    })

    # Create the line chart using st.line_chart
    st.line_chart(data.set_index('Year'))

    # Get the values for retirement age and death year
    retirement_index = retirement_age - current_age
    death_index = expectancy_life - current_age
    summary_data = {
        'Description': ['Corpous at Retirement', 'Total Invested Amount', 'Emergency funds at age'],
        'Value': ["Rs {:.0f}".format(corpus[retirement_index]), "Rs {:.0f}".format(sip_corpus[retirement_index]), "Rs {:.0f}".format(corpus[death_index])]
    }

    summary_df = pd.DataFrame(summary_data)

    # Display the summary table
    st.dataframe(summary_df, hide_index=True)

    st.warning('Great Plans! At 35, I recommend you should prioritize long-term growth investments like mutual funds (70%) and fixed deposits (15%) to build a substantial corpus for future goals like retirement. However, you also maintain a balance with gold (10%) as a hedge against inflation and insurance (5%) for risk mitigation and financial security.', icon="✅")

    # infotext = " Below is the recomended combination you can try to get a return of " + str(expected_returns * 100) + " Percent returns:" 
    # st.info(infotext, icon="ℹ️")

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    recipe = ["MUTUAL FUNDS", "GOLD", "FD", "INSURANCE"]
    data = [70, 10, 15, 5]
    colors = ['blue', 'gold', 'orange', 'green']

    wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40, colors=colors)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(recipe[i] + ": " +str(data[i]) + "%", xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)


    st.pyplot(plt)
    # Create a summary table for the values


    # Table 2
    st.subheader("Financial Instruments Distribution")
    table2 = {
         " " : ["🛒", "🛒", "🛒"],
        "Fund name": ["Amazon Gold", "Bajaj Fixed Deposits", "Insurance"],
        "Monthly Investment": ["Rs " + str(int(monthly_sip * 0.10)) , "Rs " + str(int(monthly_sip *0.15)) ,  "Rs " + str(int(monthly_sip *0.05))],
        "Anual Return": ["18.11 %", "8.01 %", "0 %"],
        "Category": ["Assest", "Secure Investment", "Security"]
    }

    df1 = pd.DataFrame(table2)
    st.dataframe(df1, hide_index=True)
    st.text("Average Returns from Above intruments: 13.02%")


    # Table 1
    st.subheader("Mutaul Funds Distribution")
    st.warning("With a long-term investment horizon, an expected return of 21.42 % from mutual funds is possible if invested in high-risk, aggressive growth funds, but it comes with higher volatility and risk.", icon="✅")

    table1 = {
        "Category": ["Large-Cap Equity Funds", "Small-Cap Equity Funds", "Mid-Cap Equity Funds", "Long-Term Debt Funds", "Balanced/Equity-Oriented Hybrid Funds"],
        "Investment Value": ["Rs " + str(int(monthly_sip *0.20)), "Rs " + str(int(monthly_sip *0.4)), "Rs " + str(int(monthly_sip *0.10)), "Rs " + str(int(monthly_sip * 0.15)), "Rs " + str(int(monthly_sip * 0.15))],
        "Average 3Y Return": ["15%", "25%", "20%", "7%", "7%"],

    }

    df = pd.DataFrame(table1)
    st.dataframe(df, hide_index=True)
    st.text("Average Returns from Mutual Funds: 21.85%")



    import streamlit as st
    import pandas as pd

    # Sample data for the tables
    large_cap_data = pd.DataFrame({
        " " : ["🛒", "🛒", "🛒"],
        "Fund name": ["ICICI Bluechip 150", "Canara Bank Super 20", "Parag Parik Momentum 150"],
        "3y Percentage": ["15%", "12%", "17%"],
        "Anual Return": ["18.11 %", "20.01 %", "22.01 %"],
        "Category": ["Equity", "Debt", "Commodities"]

    })

    small_cap_data = pd.DataFrame({
        " " : ["🛒", "🛒", "🛒"],
        "Fund name": ["ICICI Bluechip 150", "Canara Bank Super 20", "Parag Parik Momentum 150"],
        "3y Percentage": ["15%", "12%", "17%"],
        "Anual Return": ["18.11 %", "20.01 %", "22.01 %"],
        "Category": ["Equity", "Debt", "Commodities"]

    })

    mid_cap_data = pd.DataFrame({
        'Fund Name': ['Fund X', 'Fund Y', 'Fund Z'],
        'Expense Ratio': [0.7, 0.6, 0.8],
        'Returns (%)': [11.3, 12.8, 10.5]
    })

    balanced_data = pd.DataFrame({
        'Fund Name': ['Balanced 1', 'Balanced 2', 'Balanced 3'],
        'Expense Ratio': [0.4, 0.5, 0.6],
        'Returns (%)': [9.7, 8.5, 10.2]
    })

    # Collapsible tables in a grid layout
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Best Performing Large-Cap Equity Funds"):
            st.dataframe(large_cap_data)

        with st.expander("Best Performing Small-Cap Equity Funds"):
            st.table(small_cap_data)

    with col2:
        with st.expander("Best Performing Mid-Cap Equity Funds"):
            st.table(mid_cap_data)

        with st.expander("Best Performing Balanced/Equity-Oriented Hybrid Funds"):
            st.table(balanced_data)

