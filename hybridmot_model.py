import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.stats import chi2_contingency, fisher_exact,shapiro, mannwhitneyu, ttest_ind
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
from sklearn.svm import SVR
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import warnings

warnings.filterwarnings("ignore")
warnings.resetwarnings()

"""# 2. Import Data"""
df=pd.read_excel("hybrid_motivation.xlsx")

#Check null values in the dataset
df.isna().sum()
#drop irrelavant columns for anlaysis
df.drop(columns=["UID","Unnamed: 1","Unnamed: 65",'Course Code','Course','SUS',"Focus time","Region origin",'AT1 Quiz 1 Wk 4','AT1 Quiz 2 Wk 9', 'AT1 Quiz 3 Wk 13','AT 4 - Group task Wk 13'],inplace=True)
#Rename columns for better readablity and analysis
df.rename(columns={"AT2 article summary Wk 5?": "AT2", "AT 3: Critical appraisal essay Wk9": "AT3"},inplace=True)
#replacing 0s with null values
df.loc[df["AT2"] ==0, "AT2"] = np.nan
df.loc[df["AT3"] ==0, "AT3"] = np.nan
df.loc[df["ATAR"] == 0, "ATAR"] = np.nan
#Excluding the null values in the dataset
df=df.dropna(axis=0)

"""# 4. Feature Engineering : Computing Derived variables
***We are set to develop new columns that capture the nuances of Intrinsic and Extrinsic motivation, based on the responses to the IMI (Intrinsic Motivation Inventory) subscale questions. This analytical step will enable us to categorize students according to their motivational orientations. Additionally, we plan to introduce a variable to assess students' preferences for Hybrid learning modalities. This will be based on their responses to the statement 'On balance, the hybrid class is a worthwhile way of teaching,' with a rating of 3 or higher indicating agreement. To quantify Intrinsic and Extrinsic motivation, we will calculate the percentage for each by summing the relevant question responses, dividing by the total number of responses, and converting this figure into a percentage. This conversion to percentage terms enhances the readability and interpretability of the data, facilitating a clearer understanding of motivational trends among students.***
"""
df["IM_Percentage"]=((df[["I enjoyed the workshops very much.","I would describe the workshops as interesting.","While I was doing the workshops‚ I felt engaged.","I was very capable in the workshops.","After engaging with the workshops for a while‚ I felt fairly competent.","I was satisfied with my performance in the workshops.","I put a lot of effort into the workshops.","I tried very hard in the workshops.","I did the workshops because I wanted to.","I believe the workshops were of some value to me.","Looking back I'm glad I attended the workshops.","I believe doing the workshops was beneficial to me.","I think the workshops were important.","I believe I had some choice about doing the workshops.","R) I did not feel nervous at all while doing the workshops.","R) I was very relaxed in the workshops."]].sum(axis=1))/(5*16))*100
df["EM_Percentage"]=((df[["R) I thought the workshops were boring.","R) The workshops did not hold my attention at all.","R) The workshops were something I couldn't do very well.","R) I didn't put much energy into the workshops.","I was anxious while working in the workshops.","I felt pressured while doing the workshops.","R) I only came to the workshops because I felt obliged.","R) I felt I had to come to the workshops or I would fall behind."]].sum(axis=1))/(8*5))*100
df["Motivation_Type"] = df.apply(lambda x: "INTRINSIC" if ((x["IM_Percentage"] > x["EM_Percentage"]) and (x["TOTAL"]>75) and (x["AT3"]>50) and (x["ATAR"]>50)) else "EXTRINSIC", axis=1)
df["Like_Hybrid"]=df["On balance the hybrid class is a worthwhile way of teaching."].apply(lambda x:"YES" if x>=3 else "NO")

"""
# 7. Variable transformation and encoding
# 7.1. Categorical encoding
# 7.1.1. Binary encoding
"""
#After deriving the relevant columns, we will now select the columns that are relevant to our analysis.
hybrid_data=df[["Mode","Campus","ATAR","Course Weighted Average","Age","Gender","IMI - Interest/Enjoyment","IMI - Perceived Competence","IMI - Effort/Importance","IMI - Pressure/Tension","IMI - Perceived Choice","IMI - Value/Usefulness","IMI - Relatedness","IMI Total","IM_Percentage","EM_Percentage","Motivation_Type","Like_Hybrid","AT2","AT3","TOTAL"]]
hybrid_data["Mode_transformed"]=hybrid_data["Mode"].apply(lambda x:1 if x=="Hybrid/Class.com" else 0)
hybrid_data["Gender_transformed"]=hybrid_data["Gender"].apply(lambda x:1 if x=="Female" else 0)
hybrid_data["Motivation_type_transformed"]=hybrid_data["Motivation_Type"].apply(lambda x:1 if x=="INTRINSIC" else 0)
hybrid_data["Like_Hybrid_transformed"]=hybrid_data["Like_Hybrid"].apply(lambda x:1 if x=="YES" else 0)
hybrid_data

"""# 7.1.2. One-hot encoding"""
# Perform one-hot encoding
hybrid_data_transformed_classification = pd.get_dummies(hybrid_data, columns=['Campus'])

# 7.2.1. Standard scaling
"""# Columns to scale"""
columns_to_scale = ["ATAR", "Course Weighted Average", "Age", "IMI - Interest/Enjoyment",
                    "IMI - Perceived Competence", "IMI - Effort/Importance", "IMI - Pressure/Tension",
                    "IMI - Perceived Choice", "IMI - Value/Usefulness", "IMI - Relatedness",
                    "IMI Total", "IM_Percentage", "EM_Percentage", 'AT2', 'TOTAL']

# Initialize the StandardScaler
sc=StandardScaler()

hybrid_data_transformed_classification[columns_to_scale]=sc.fit_transform(hybrid_data_transformed_classification[columns_to_scale])



# Check the DataFrame
hybrid_data_transformed_classification.columns

"""# 8. Data Modelling"""



X = hybrid_data_transformed_classification.drop(columns=["Mode", "Gender", "Motivation_Type", "Like_Hybrid","AT3"])  # Example feature columns
y = hybrid_data_transformed_classification['AT3']  # Target variable


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y,train_size=0.957 ,random_state=1)


"""# 9. Support Vector Machine"""

# Assuming X_train, X_test, y_train, y_test are defined

# Define parameter grid for cross-validation
param_grid = {
    'C': [0.1, 1, 10, 100],  # Regularization parameter
    'gamma': [1, 0.1, 0.01, 0.001],  # Kernel coefficient
    'epsilon': [0.1, 0.2, 0.5, 1],
    "kernel":["linear","rbf"]
}

"""***We use Support vector Machine because we have limited data and SVM works well and is suited For datasets of smaller size***"""

# Assuming you have a DataFrame 'df' with features and a target variable
# Replace 'features' with your feature columns and 'target' with your target column
X = hybrid_data_transformed_classification.drop(['Motivation_type_transformed',"Motivation_Type","Mode", "Gender", "Motivation_Type", "Like_Hybrid"], axis=1)  # Example feature columns
y = hybrid_data_transformed_classification['Motivation_type_transformed']  # Target variable


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=1)


# Define the model
svm_model = SVC(random_state=42)

# Define the hyperparameter grid
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': [1, 0.1, 0.01, 0.001],
    "kernel":["linear","rbf"]
}

# Grid search
grid_search = GridSearchCV(svm_model, param_grid, cv=10, scoring='accuracy')

# Fit the model
grid_search.fit(X_train, y_train)


# fit the optimal fine-tuned model
best_model = SVC(**grid_search.best_params_,random_state=1)
best_model.fit(X_train,y_train)