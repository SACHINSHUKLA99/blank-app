import streamlit as st

# Setting the title for the app
st.title("Personal Details Form")

# Creating the form using streamlit form structure
with st.form("personal_details_form"):
    # Input fields for personal details
    name = st.text_input("Enter your full name")
    age = st.number_input("Enter your age", min_value=1, max_value=120)
    gender = st.radio("Select your gender", ("Male", "Female", "Other"))
    email = st.text_input("Enter your email")

    # Submit button
    submit = st.form_submit_button("Submit")

# After submission
if submit:
    st.success(f"Form Submitted Successfully!")
    st.write(f"**Name**: {name}")
    st.write(f"**Age**: {age}")
    st.write(f"**Gender**: {gender}")
    st.write(f"**Email**: {email}")
