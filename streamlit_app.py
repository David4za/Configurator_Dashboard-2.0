import pandas as pd
import streamlit as st
import openpyxl

# Title
st.title("Standard Dunker Motor & Gearbox Configurator")

# Upload file
uploaded_file = st.file_uploader("Upload Dunker Synoptik Table", type=['xlsm', 'xlsx'])

if uploaded_file:
    try:
        # Read the file
        motor_df = pd.read_excel(uploaded_file, sheet_name="Motor Type", engine="openpyxl")
        gearbox_df = pd.read_excel(uploaded_file, sheet_name="Gearboxes", engine="openpyxl")
        
        # Step 1: Select Motor
        st.subheader("Step 1: Select Motor")
        motor_types = sorted(motor_df['Motor Type'].unique(), reverse=True)  # Descending order
        selected_motor = st.selectbox("Select Motor", motor_types, key="motor_select")

        if selected_motor:
            st.success(f"Motor Type Selected: {selected_motor}")
            
            # Filter for selected motor
            filtered_motor_df = motor_df[motor_df['Motor Type'] == selected_motor]

            # Step 2: Select Motor Properties
            with st.expander("Step 2: Configure Motor Properties"):
                st.info("Select properties for the chosen motor.")
                selected_motor_properties = {}  # To store motor properties
                
                for col in motor_df.columns:
                    if col != "Motor Type":
                        unique_values = filtered_motor_df[col].dropna().unique()
                        sorted_values = sorted(unique_values, reverse=True)
                        selected_value = st.selectbox(
                            f"Select {col}", sorted_values, key=f"motor_{col}"
                        )
                        selected_motor_properties[col] = selected_value
                        filtered_motor_df = filtered_motor_df[filtered_motor_df[col] == selected_value]

            # Step 3: Select Gearbox
            compatible_gearboxes = gearbox_df[gearbox_df['Motor Type'] == selected_motor]
            if not compatible_gearboxes.empty:
                with st.expander("Step 3: Configure Gearbox"):
                    st.info("Select gearbox properties compatible with the motor.")
                    selected_gearbox_properties = {}
                    
                    for col in gearbox_df.columns:
                        if col != "Motor Type":
                            unique_values = compatible_gearboxes[col].dropna().unique()
                            sorted_values = sorted(unique_values, reverse=True)
                            selected_value = st.selectbox(
                                f"Select {col}", sorted_values, key=f"gearbox_{col}"
                            )
                            selected_gearbox_properties[col] = selected_value
                            compatible_gearboxes = compatible_gearboxes[
                                compatible_gearboxes[col] == selected_value
                            ]
            else:
                st.warning("No compatible gearboxes found for the selected motor.")

            # Step 4: Final Summary
            if selected_motor_properties and selected_gearbox_properties:
                st.subheader("Final Configuration")
                st.write("Here is your selected motor + gearbox combination:")
                
                # Combine selected motor and gearbox properties
                final_selection = {
                    "Motor Type": selected_motor,
                    **selected_motor_properties,
                    **selected_gearbox_properties,
                }
                st.table(pd.DataFrame([final_selection]))
                
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload an Excel file.")
