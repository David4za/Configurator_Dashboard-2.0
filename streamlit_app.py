import pandas as pd
import streamlit as st
import openpyxl

# Title
st.title("Standard Dunker Motor & Gearbox Configurator")

uploaded_file = st.file_uploader("Upload Dunker Synoptik file")

if uploaded_file:
    try:
        #get df
        motor_df = pd.read_excel(uploaded_file, sheet_name= "Motor Type", engine='openpyxl')
        gearbox_df = pd.read_excel(uploaded_file, sheet_name= "Gearboxes", engine='openpyxl')

        st.subheader('Step 1: Select Motor Type')
        motor_types = sorted(motor_df['Motor Type'].unique(), reverse=True)
        selected_motor = st.selectbox("Select Motor", motor_types, key= f"motor_select")

        if selected_motor:
            st.success(f"Motor Type Selected: {selected_motor}")

            #Filter based on selected motor
            filtered_motor_df = motor_df[motor_df['Motor Type'] == selected_motor]

            #Step 2: Motor Properties
            with st.expander('Step 2: Configure Motor properties'):
                st.info("Select properties for the selected motor")
                selected_motor_properties = {} #To store the option for display at the end

                for col in motor_df.columns:
                    if col != "Motor Type":
                        unique_values = filtered_motor_df[col].dropna().unique()
                        sorted_values = sorted(unique_values, reverse=False)
                        selected_value = st.selectbox(f'Select {col}', sorted_values, key=f'motor_{col}')
                        selected_motor_properties[col] = selected_value

                        #update filtered_df
                        filtered_motor_df = filtered_motor_df[filtered_motor_df[col] == selected_value]

            #Step 3: Gearbox Selection and Properties
            compatible_gearboxes = gearbox_df[gearbox_df['Motor Type'] == selected_motor]
            if not compatible_gearboxes.empty:
                with st.expander('Step 3: Configure Gearbox'):
                    st.info(" Select gearbox properties compatible with selected motor")
                    selected_gearbox_properties = {}

                    for col in gearbox_df.columns:
                        if col != 'Motor Type':
                            unique_values = compatible_gearboxes[col].dropna().unique()
                            sorted_values = sorted(unique_values, reverse=False)
                            selected_value = st.selectbox(f'Select {col}', sorted_values, key=f'gearbox_{col}')
                            selected_gearbox_properties[col] = selected_value

                            #update filter
                            compatible_gearboxes = compatible_gearboxes[compatible_gearboxes[col] == selected_value]
            
            else:
                st.warning("No compatible gearboxes found for the selected motor")

            #step 4: FInal summary
            if selected_motor_properties and selected_gearbox_properties:
                st.subheader('Final Configuration')
                st.write("Here is your selected Motor Type + Gearbox combination")

                #combine the motor and gearbox
                final_selection = {'Motor Type': selected_motor,
                                   **selected_motor_properties,
                                   **selected_gearbox_properties
                                   }
                #convert to df
                final_selection_df = pd.DataFrame([final_selection])

                #display
                st.table(final_selection_df)

                #CSV download
                csv_data = final_selection_df.to_csv(index=False)
                st.download_button(
                    label="Download Configuration as CSV",
                    data=csv_data,
                    file_name= f'{selected_motor}_motor_gearbox_configuration.csv',
                    mime="txt/csv"
                )

    except Exception as e:
        st.error(f'An error occurred while processing the file: {e}')
    
else:
    st.info("Please upload the Excel file ")

