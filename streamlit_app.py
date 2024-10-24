import streamlit as st
import pandas as pd

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
        expenses = st.number_input("Expenses", min_value=1000, step=1)
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

    # # Display the calculated results
    # st.write("## Calculated Results")
    # st.table(results)
