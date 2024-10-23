import streamlit as st

# Setting the title for the app
st.title("Retrirement Plan")

# Creating the form using streamlit form structure
with st.form("retirement_plan_form"):
    # Input fields for personal details
    name = st.number_input("Current Age")
    age = st.number_input("Life Expectancy")
    gender = st.number_input("Retirement Age")
    email = st.number_input("Expected Return %")

    # Submit button
    submit = st.form_submit_button("Submit")

# After submission
if submit:
    st.success(f"Form Submitted Successfully!")
    st.write(f"**Name**: {name}")
    st.write(f"**Age**: {age}")
    st.write(f"**Gender**: {gender}")
    st.write(f"**Email**: {email}")
