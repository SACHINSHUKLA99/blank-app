import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# Initialize the session state to control form visibility and dynamic fields
if 'dynamic_fields' not in st.session_state:
    st.session_state.dynamic_fields = []
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

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
        st.success(f"New field '{custom_title}' added. Please see the new field above.")
    else:
        st.warning("Please provide both a title and a label for the dynamic field!")

# Title of the app
st.title("Retirement Planning Form")

# Show form only if not submitted
if not st.session_state.form_submitted:
    # Main form layout with static inputs
    with st.form("retirement_planning_form"):
        # Create two columns for the static input fields
        col1, col2 = st.columns(2)

        # First column (left side) - static fields
        with col1:
            current_age = st.number_input("Current Age", min_value=1, max_value=120, step=1)
            present_portfolio = st.number_input("Present Portfolio (₹)", min_value=1, step=1)
            income = st.number_input("Income (₹)", min_value=1, step=1)
            current_expenditure = st.number_input("Upfront Investment (₹)", min_value=0.0, step=1000.0)

        # Second column (right side) - static fields
        with col2:
            expense_post_retirement = st.number_input("Expense Post Retirement (₹)", min_value=1000, step=1)
            house_expense = st.number_input("House Expense (at 30) (₹)", min_value=1000, step=1)
            expenses = st.number_input("Expenses", min_value=1000, step=1)
            retirement_age = st.number_input("Retirement Age", min_value=1, max_value=120, step=1)

        # Dynamic fields based on session state
        st.subheader("Goals")
        dynamic_col1, dynamic_col2 = st.columns(2)  # Create two columns for dynamic fields
        
        # Loop through dynamic fields and display them in two columns
        for i, field in enumerate(st.session_state.dynamic_fields):
            with dynamic_col1 if i % 2 == 0 else dynamic_col2:
                value1 = st.number_input(f"Value 1 for {field['title']}", key=field['input_key_value1'])
                value2 = st.number_input(f"Value 2 for {field['title']}", key=field['input_key_value2'])

        # Submit button
        submit = st.form_submit_button("Submit")
else:
    # This code will execute when the form is submitted
    st.success("Form submitted successfully!")

# After submission, display the calculations and results
if submit:
    # Set the form submitted state to True
    st.session_state.form_submitted = True
    
    # Converting expenses input to a dictionary (modify as necessary)
    expenses_dict = {current_age + i: expenses for i in range(0, retirement_age - current_age)}

    # Calculate the corpus for each year
    start_year = 2024  # Assuming the current year is 2024
    expectancy_life = 85  # Set life expectancy here
    years = range(start_year, start_year + expectancy_life - current_age + 1)
    corpus = [present_portfolio]
    sip_corpus = [0] * len(years)
    swp_corpus = [0] * len(years)
    invested_sum = 0
    withdrawn_sum = 0

    expected_returns = 0.08  # Assuming 8% annual return on investment
    monthly_sip = 10000  # Set this according to your inputs
    monthly_swp = 0  # Modify as needed
    inflation_rate = 0.03  # Assuming 3% annual inflation rate

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
        'Description': ['Corpus at Retirement', 'Total Invested Amount', 'Emergency funds at age'],
        'Value': ["Rs {:.0f}".format(corpus[retirement_index]), "Rs {:.0f}".format(sip_corpus[retirement
