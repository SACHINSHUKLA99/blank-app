import streamlit as st

# Initialize the session state to store dynamic fields and subfields if not already present
if 'dynamic_fields' not in st.session_state:
    st.session_state.dynamic_fields = []

# Function to add a new dynamic field with custom title, label, and input type
def add_dynamic_field(title, label, input_type):
    new_field = {
        'title': title,
        'label': label,
        'input_type': input_type,
        'input_key': f"input_{len(st.session_state.dynamic_fields)}",
        'subfields': []  # List to store subfields
    }
    st.session_state.dynamic_fields.append(new_field)

# Function to add a subfield to a specific dynamic field
def add_subfield(dynamic_field_index, subfield_label, subfield_input_type):
    subfield = {
        'label': subfield_label,
        'input_type': subfield_input_type,
        'input_key': f"subfield_{len(st.session_state.dynamic_fields[dynamic_field_index]['subfields'])}_{dynamic_field_index}"
    }
    st.session_state.dynamic_fields[dynamic_field_index]['subfields'].append(subfield)

# Title of the app
st.title("Retirement Planning Form with Dynamic Fields and Sub-inputs")

# Main form layout with static inputs
with st.form("retirement_planning_form"):
    col1, col2 = st.columns(2)

    # First column (left side) - static fields
    with col1:
        current_age = st.number_input("Current Age", min_value=1, max_value=120, step=1)
        life_expectancy = st.number_input("Life Expectancy", min_value=1, max_value=120, step=1)
        retirement_age = st.number_input("Retirement Age", min_value=1, max_value=120, step=1)
        current_expenditure = st.number_input("Current Expenditure (₹ per year)", min_value=0.0, step=1000.0)

    # Second column (right side) - static fields
    with col2:
        expected_return = st.number_input("Expected Return %", min_value=0.0, max_value=100.0, step=0.1)
        risk_appetite = st.selectbox("Risk Appetite", ("Low", "Moderate", "High"))
        current_lumpsum = st.number_input("Current Lumpsum (₹ Savings/Investments)", min_value=0.0, step=1000.0)
        inflation = st.number_input("Inflation Rate %", min_value=0.0, max_value=100.0, step=0.1, value=6.0)

    # Dynamic fields based on session state
    st.subheader("Dynamic Fields")
    
    # Loop through dynamic fields and render them with subfields
    for i, field in enumerate(st.session_state.dynamic_fields):
        st.write(f"**{field.get('title', 'Untitled')}**")

        # Render the main input field
        input_type = field.get('input_type', 'Text')  # Default to 'Text' if not present
        
        if input_type == 'Text':
            st.text_input(field.get('label', 'No Label'), key=field.get('input_key'))
        elif input_type == 'Number':
            st.number_input(field.get('label', 'No Label'), key=field.get('input_key'))
        
        # Sub-input fields
        st.write("Subfields:")
        for subfield in field['subfields']:
            sub_input_type = subfield.get('input_type', 'Text')
            if sub_input_type == 'Text':
                st.text_input(subfield.get('label', 'No Subfield Label'), key=subfield.get('input_key'))
            elif sub_input_type == 'Number':
                st.number_input(subfield.get('label', 'No Subfield Label'), key=subfield.get('input_key'))
        
        # Inputs for adding a new subfield to the dynamic field
        subfield_label = st.text_input(f"Subfield Label for {field['title']}", key=f"subfield_label_{i}")
        subfield_input_type = st.selectbox(f"Subfield Input Type for {field['title']}", ["Text", "Number"], key=f"subfield_input_type_{i}")
        if st.button(f"Add Subfield to {field['title']}"):
            add_subfield(i, subfield_label, subfield_input_type)

    # Submit button
    submit = st.form_submit_button("Submit")

# Input to create new dynamic field
st.subheader("Add Custom Dynamic Field")
custom_title = st.text_input("Enter Field Title")
custom_label = st.text_input("Enter Field Label")
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
        
        # Display subfield values
        for subfield in field['subfields']:
            st.write(f"**{subfield['label']}**: {st.session_state.get(subfield['input_key'], '')}")
