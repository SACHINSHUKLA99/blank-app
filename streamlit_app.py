import streamlit as st

# Initialize the session state to store dynamic fields if it's not already present
if 'dynamic_fields' not in st.session_state:
    st.session_state.dynamic_fields = []

# Function to add a new dynamic field
def add_dynamic_field():
    new_field = {
        'title': f"Dynamic Field {len(st.session_state.dynamic_fields) + 1}",
        'label': f"Label {len(st.session_state.dynamic_fields) + 1}",
        'input_key': f"input_{len(st.session_state.dynamic_fields)}"
    }
    st.session_state.dynamic_fields.append(new_field)

# Title of the app
st.title("Retirement Planning Form with Dynamic Fields")

# Create two columns for the form layout
col1, col2 = st.columns(2)

# Main form for static inputs
with st.form("retirement_planning_form"):
    # First column (left side)
    with col1:
        current_age = st.number_input("Current Age", min_value=1, max_value=120, step=1)
        life_expectancy = st.number_input("Life Expectancy", min_value=1, max_value=120, step=1)
        retirement_age = st.number_input("Retirement Age", min_value=1, max_value=120, step=1)
        current_expenditure = st.number_input("Current Expenditure (₹ per year)", min_value=0.0, step=1000.0)

    # Second column (right side)
    with col2:
        expected_return = st.number_input("Expected Return %", min_value=0.0, max_value=100.0, step=0.1)
        risk_appetite = st.selectbox("Risk Appetite", ("Low", "Moderate", "High"))
        current_lumpsum = st.number_input("Current Lumpsum (₹ Savings/Investments)", min_value=0.0, step=1000.0)
        inflation = st.number_input("Inflation Rate %", min_value=0.0, max_value=100.0, step=0.1, value=6.0)
    
    # Dynamic fields based on session state
    st.subheader("Dynamic Fields")
    for field in st.session_state.dynamic_fields:
        st.text_input(field['label'], key=field['input_key'])

    # Submit button (below both columns)
    submit = st.form_submit_button("Submit")

# Button to add new dynamic fields
if st.button("Add Dynamic Field"):
    add_dynamic_field()

# After submission, display the entered data
if submit:
    st.success("Form Submitted Successfully!")
    st.write(f"**Current Age**: {current_age}")
    st.write(f"**Life Expectancy**: {life_expectancy}")
    st.write(f"**Retirement Age**: {retirement_age}")
    st.write(f"**Expected Return %**: {expected_return}%")
    st.write(f"**Current Expenditure**: ₹{current_expenditure}")
    st.write(f"**Risk Appetite**: {risk_appetite}")
    st.write(f"**Current Lumpsum**: ₹{current_lumpsum}")
    st.write(f"**Inflation Rate**: {inflation}%")

    # Display dynamic field values
    st.write("### Dynamic Field Inputs")
    for field in st.session_state.dynamic_fields:
        st.write(f"**{field['label']}**: {st.session_state[field['input_key']]}")

