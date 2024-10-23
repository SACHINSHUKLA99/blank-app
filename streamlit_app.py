import streamlit as st

# Setting the title for the app
st.title("Retirement Plan")

# Creating the form using streamlit form structure
with st.form("retirement_plan_form"):
    current_age = st.number_input("Current Age", min_value=1, max_value=120, step=1)
    life_expectancy = st.number_input("Life Expectancy", min_value=1, max_value=120, step=1)
    retirement_age = st.number_input("Retirement Age", min_value=1, max_value=120, step=1)
    expected_return = st.number_input("Expected Return %", min_value=0.0, max_value=100.0, step=0.1)
    current_expenditure = st.number_input("Current Expenditure (per year)", min_value=0.0, step=1000.0)
    
    # Risk appetite as a select box with predefined options
    risk_appetite = st.selectbox("Risk Appetite", ("Low", "Moderate", "High"))
    
    current_lumpsum = st.number_input("Current Lumpsum (Savings/Investments)", min_value=0.0, step=1000.0)
    
    # Inflation with a default value of 6%
    inflation = st.number_input("Inflation Rate %", min_value=0.0, max_value=100.0, step=0.1, value=6.0)

    # Submit button
    submit = st.form_submit_button("Submit")

# After submission
if submit:
    st.success("Form Submitted Successfully!")
    st.write(f"**Current Age**: {current_age}")
    st.write(f"**Life Expectancy**: {life_expectancy}")
    st.write(f"**Retirement Age**: {retirement_age}")
    st.write(f"**Expected Return %**: {expected_return}%")
    st.write(f"**Current Expenditure**: {current_expenditure}")
    st.write(f"**Risk Appetite**: {risk_appetite}")
    st.write(f"**Current Lumpsum**: {current_lumpsum}")
    st.write(f"**Inflation Rate**: {inflation}%")
