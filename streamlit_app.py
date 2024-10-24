import streamlit as st

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

# Function to add a new dynamic field with custom title and label
def add_dynamic_field(title):
    new_field = {
        'title': title,
        'input_key': f"input_{len(st.session_state.dynamic_fields)}"
    }
    st.session_state.dynamic_fields.append(new_field)

# Title of the app
st.title("Retirement Planning Form with Custom Dynamic Fields")

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
            st.write(f"**{field.get('title', 'Untitled')}**")
            st.number_input(field.get('title', 'No Label'), key=field.get('input_key'))

    # Submit button
    submit = st.form_submit_button("Submit")

# Input to create new dynamic field
st.subheader("Add Goals")
custom_title = st.text_input("Enter Goal Name")

# Button to add new dynamic field
if st.button("Add Dynamic Field"):
    if custom_title :
        add_dynamic_field(custom_title)
    else:
        st.warning("Please provide both a title and a label for the dynamic field!")

# After submission, display the entered data
if submit:
    st.success("Form Submitted Successfully!")
    st.write(f"**Current Age**: {current_age}")
    st.write(f"**Present Portfolio**: ₹{present_portfolio}")
    st.write(f"**Income**: ₹{income}")
    st.write(f"**House Expense**: ₹{house_expense}")
    st.write(f"**Expense Post Retirement**: ₹{expense_post_retirement}")
    st.write(f"**Expenses**: ₹{expenses}")
    st.write(f"**Retirement Age**: {retirement_age}")

    # Display dynamic field values
    st.write("### Dynamic Field Inputs")
    for field in st.session_state.dynamic_fields:
        st.write(f"**{field['label']}**: {st.session_state.get(field['input_key'], '')}")
