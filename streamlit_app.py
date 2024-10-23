import streamlit as st

# Initialize the session state to store dynamic fields if it's not already present
if 'dynamic_fields' not in st.session_state:
    st.session_state.dynamic_fields = []

# Function to add a new dynamic field with custom title, label, and input type
def add_dynamic_field(title, label, input_type):
    new_field = {
        'title': title,
        'label': label,
        'input_type': input_type,
        'input_key': f"input_{len(st.session_state.dynamic_fields)}"
    }
    st.session_state.dynamic_fields.append(new_field)

# Title of the app
st.title("Retirement Planning Form with Custom Dynamic Fields")

# Main form layout with static inputs
with st.form("retirement_planning_form"):
    col1, col2 = st.columns(2)

    # First column (left side) - static fields
    with col1:
        current_age = st.number_input("Age", min_value=1, max_value=120, step=1)
        life_expectancy = st.number_input("Monthly Income (₹)", min_value=1, max_value=120, step=1)
        retirement_age = st.number_input("Monthly Expenditure (₹)", min_value=1, max_value=120, step=1)
        current_expenditure = st.number_input("Upfront investment (₹)", min_value=0.0, step=1000.0)

    # Dynamic fields based on session state
    st.subheader("Goals")
    
    # Updated snippet to safely handle dynamic fields
    for field in st.session_state.dynamic_fields:
        st.write(f"**{field.get('title', 'Untitled')}**")
        
        # Safely retrieve the input_type and handle errors
        input_type = field.get('input_type', 'Text')  # Default to 'Text' if not present
        
        if input_type == 'Text':
            st.text_input(field.get('label', 'No Label'), key=field.get('input_key'))
        elif input_type == 'Number':
            st.number_input(field.get('label', 'No Label'), key=field.get('input_key'))

    # Submit button
    submit = st.form_submit_button("Submit")

# Input to create new dynamic field
st.subheader("Add Goals")
custom_title = st.text_input("Enter Goal Title")
custom_label = st.text_input("Enter Goal Name")
input_type = st.selectbox("Select Input Type", ("Text", "Number"))

# Button to add new dynamic field
if st.button("Add Dynamic Field"):
    if custom_title and custom_label:
        add_dynamic_field(custom_title, custom_label, input_type)
    else:
        st.warning("Please provide both a title and a label for the dynamic field!")

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
        st.write(f"**{field['label']}**: {st.session_state.get(field['input_key'], '')}")
