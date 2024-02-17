import streamlit as st
import pandas as pd
import pickle
import hybridmot_model as hm

#Creating Test data for testing the Model
atar = 99.99
wam=76
Age = 27
ie=4
pc=5
ei=4
pt = 5
pc=4
vu=3
rel=4
imit=ie+pc+ei+pt+pc+vu+rel
imp = 75
emp=35
at2 = 18
at3 = 90
total=93
Mode = "Hybrid/Class.com"
Gender = "Female"
lh = "YES"
campus = "Bundoora"

data = {
    "ATAR": [atar],
    "Course Weighted Average": [wam],
    "Age": [Age],
    "IMI - Interest/Enjoyment": [ie],
    "IMI - Perceived Competence": [pc],
    "IMI - Effort/Importance": [ei],
    "IMI - Pressure/Tension": [pt],
    "IMI - Perceived Choice": [pc],
    "IMI - Value/Usefulness": [vu],
    "IMI - Relatedness": [rel],
    "IMI Total": [imit],
    "IM_Percentage": [imp],
    "EM_Percentage": [emp],
    "AT2": [at2],
    "AT3": [at3],
    "TOTAL": [total],
    "Mode": [Mode],
    "Gender": [Gender],
    "LKH": [lh],
    "Campus": [campus]
}

test_data = pd.DataFrame(data)
if campus == "Bundoora":
    test_data["Campus_Albury-Wodonga"]=0
    test_data["Campus_Bendigo"]=0
    test_data["Campus_Bundoora"] = 1
    test_data["Campus_Mildura"]=0
elif campus == "Bendigo":
    test_data["Campus_Albury-Wodonga"]=0
    test_data["Campus_Bendigo"]=1
    test_data["Campus_Bundoora"] = 0
    test_data["Campus_Mildura"]=0
elif campus == "Mildura":
    test_data["Campus_Albury-Wodonga"]=0
    test_data["Campus_Bendigo"]=0
    test_data["Campus_Bundoora"] = 0
    test_data["Campus_Mildura"]=1
else:
  test_data["Campus_Albury-Wodonga"]=1
  test_data["Campus_Bendigo"]=0
  test_data["Campus_Bundoora"] = 0
  test_data["Campus_Mildura"]=0


if Mode=="Hybrid/Class.com":
  test_data["Mode"]=1
else:
  test_data["Mode"]=0

if Gender=="Female":
  test_data["Gender"]=1
else:
  test_data["Gender"]=0

if lh=="YES":
  test_data["LKH"]=1
else:
  test_data["LKH"]=0
test_data.drop(columns=["Campus"],inplace=True)
test_data[['ATAR',"Course Weighted Average" ,'Age', "IMI - Interest/Enjoyment","IMI - Perceived Competence","IMI - Effort/Importance","IMI - Pressure/Tension","IMI - Perceived Choice","IMI - Value/Usefulness",'IMI - Relatedness',"IMI Total" ,'IM_Percentage',"EM_Percentage" ,'AT2',"TOTAL"]]=hm.sc.transform(test_data[['ATAR',"Course Weighted Average" ,'Age', "IMI - Interest/Enjoyment","IMI - Perceived Competence","IMI - Effort/Importance","IMI - Pressure/Tension","IMI - Perceived Choice","IMI - Value/Usefulness",'IMI - Relatedness',"IMI Total" ,'IM_Percentage',"EM_Percentage" ,'AT2',"TOTAL"]])
# Load the saved model from the specified path
model_file_path = "FINE_TUNED_HYBRID_MOTIVATION_VECTOR_MACHINE.pkl"
with open(model_file_path, 'rb') as file:
    loaded_model = pickle.load(file)

#
    
st.title("La Trobe University Student Survey: Teaching & Motivation Insights")

# Define the slider labels with corresponding emojis
options = {
    1: '😭',  # Lowest level of interest/enjoyment
    2: '🙁',
    3: '😐',
    4: '😊',
    5: '😃'   # Highest level of interest/enjoyment
}

fname=st.text_input("Whats the first name on your student ID 🤔❓")
lname=st.text_input("Whats the last name on your student ID 🤔❓")

# Create a three-column layout
col1, col2, col3= st.columns(3)

# Campus select box in the first column
with col1:
    campus = st.selectbox('Which Campus are you from 🤔❓', ['Bundoora', 'Bendigo', 'Mildura', 'Albury-Wodonga'])

# Gender select box in the second column
with col2:
    gender = st.selectbox('Gender', ['Female', 'Male'])

# Mode of study select box in the third column
with col3:
    mode = st.selectbox('What\'s your Mode of study 🤔❓', ['Hybrid/Class.com', 'Online'])
age = st.number_input('How old are you 🤔❓', 0, 100, 27)
atar = st.number_input('How much is your ATAR Score 🤔❓', 0.0, 100.0, 99.99)
wam = st.number_input('How much is your Course Weighted Average 🤔❓', 0, 100, 76) 
col4,col5 = st.columns(2)
with col4:
    at2 = st.number_input('Assesment Term 2 Grades', 0, 100, 18)
with col5:
    at3 = st.number_input('Assesment Term 3 Grades', 0, 100, 90)
total = st.number_input('Total Grade', 0, 100, 93)
# Create sliders for each IMI component
ie = st.select_slider('Interest/Enjoyment', options=list(options.keys()), format_func=lambda x: options[x])
pc = st.select_slider('Perceived Competence', options=list(options.keys()), format_func=lambda x: options[x])
ei = st.select_slider('Effort/Importance', options=list(options.keys()), format_func=lambda x: options[x])
pt = st.select_slider('Pressure/Tension', options=list(options.keys()), format_func=lambda x: options[x])
vu = st.select_slider('Value/Usefulness', options=list(options.keys()), format_func=lambda x: options[x])
rel = st.select_slider('Relatedness', options=list(options.keys()), format_func=lambda x: options[x])
imp = st.slider('How much do you love this subject 🤔❓', 0, 100, 75)
emp = st.slider('On what percentage did you hate this subject 🤔❓', 0, 100, 35)

# Calculate IMI Total
imit = ie + pc + ei + pt + pc + vu + rel

# Prepare the data dictionary
data = {
    "ATAR": [atar],
    "Course Weighted Average": [wam],
    "Age": [age],
    "IMI - Interest/Enjoyment": [ie],
    "IMI - Perceived Competence": [pc],
    "IMI - Effort/Importance": [ei],
    "IMI - Pressure/Tension": [pt],
    "IMI - Perceived Choice": [pc],
    "IMI - Value/Usefulness": [vu],
    "IMI - Relatedness": [rel],
    "IMI Total": [imit],
    "IM_Percentage": [imp],
    "EM_Percentage": [emp],
    "AT2": [at2],
    "AT3": [at3],
    "TOTAL": [total],
    "Mode": [mode],
    "Gender": [gender],
    "LKH": [lh],
    "Campus": [campus]
}

# Convert to DataFrame
test_data = pd.DataFrame(data)

# Preprocess campus information
test_data["Campus_Albury-Wodonga"] = 0
test_data["Campus_Bendigo"] = 0
test_data["Campus_Bundoora"] = 0
test_data["Campus_Mildura"] = 0

if campus == "Bundoora":
    test_data["Campus_Bundoora"] = 1
elif campus == "Bendigo":
    test_data["Campus_Bendigo"] = 1
elif campus == "Mildura":
    test_data["Campus_Mildura"] = 1
else:  # Albury-Wodonga
    test_data["Campus_Albury-Wodonga"] = 1

# Preprocess mode information
test_data["Mode"] = 1 if mode == "Hybrid/Class.com" else 0

# Preprocess gender information
test_data["Gender"] = 1 if gender == "Female" else 0

# Preprocess LKH information
test_data["LKH"] = 1 if lh == "YES" else 0

# Drop the original 'Campus' column as it's no longer needed after one-hot encoding
test_data.drop(columns=["Campus"], inplace=True)

# Assuming 'sc' is properly defined and trained
# Scale the numerical features
# Define which columns need to be scaled
# Replace 'columns_to_scale' with the actual columns that

test_data[['ATAR',"Course Weighted Average" ,'Age', "IMI - Interest/Enjoyment","IMI - Perceived Competence","IMI - Effort/Importance","IMI - Pressure/Tension","IMI - Perceived Choice","IMI - Value/Usefulness",'IMI - Relatedness',"IMI Total" ,'IM_Percentage',"EM_Percentage" ,'AT2',"TOTAL"]]=hm.sc.transform(test_data[['ATAR',"Course Weighted Average" ,'Age', "IMI - Interest/Enjoyment","IMI - Perceived Competence","IMI - Effort/Importance","IMI - Pressure/Tension","IMI - Perceived Choice","IMI - Value/Usefulness",'IMI - Relatedness',"IMI Total" ,'IM_Percentage',"EM_Percentage" ,'AT2',"TOTAL"]])
result=loaded_model.predict(test_data.values)[0]



# Custom CSS to inject into the Streamlit page
button_style = """
<style>
/* Create a class for the button */
.button-36 {
  background-image: linear-gradient(92.88deg, #455EB5 9.16%, #5643CC 43.89%, #673FD7 64.72%);
  border-radius: 8px;
  border-style: none;
  box-sizing: border-box;
  color: #FFFFFF;
  cursor: pointer;
  flex-shrink: 0;
  font-family: "Inter UI","SF Pro Display",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen,Ubuntu,Cantarell,"Open Sans","Helvetica Neue",sans-serif;
  font-size: 16px;
  font-weight: 500;
  height: 4rem;
  padding: 0 1.6rem;
  text-align: center;
  text-shadow: rgba(0, 0, 0, 0.25) 0 3px 8px;
  transition: all .5s;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}

/* Hover state */
.button-36:hover {
  box-shadow: rgba(80, 63, 205, 0.5) 0 1px 30px;
  transition-duration: .1s;
}

/* Apply the styles to Streamlit button */
div.stButton > button {
    box-shadow: none !important;
    border-radius: 8px !important;
    font-family: "Inter UI", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    height: 4rem !important;
    padding: 0 1.6rem !important;
    text-align: center !important;
    text-shadow: rgba(0, 0, 0, 0.25) 0 3px 8px !important;
    transition: all .5s !important;
    background-image: linear-gradient(92.88deg, #455EB5 9.16%, #5643CC 43.89%, #673FD7 64.72%) !important;
    color: #FFFFFF !important;
    border-style: none !important;
    line-height: 4rem !important;
    width: 100% !important;
}
</style>
"""

# Inject custom CSS with Markdown
st.markdown(button_style, unsafe_allow_html=True)

if st.button("Assess Student's Motivation Type 🤔❓"):
    if result == 1:
        if gender == "Female":
            message = "The Student is Intrinsically Motivated For her Academics"
        else:  # Assuming gender == "Male"
            message = "The Student is Intrinsically Motivated For his Academics"
        # Display in green
        st.info(message, icon="😃")
    else:
        if gender == "Male":
            message = "The Student is Extrinsically Motivated For his Academics"
        else:  # Assuming gender == "Female"
            message = "The Student is Extrinsically Motivated For her Academics"
        # Display in red
        st.info(message, icon="☹️")
