import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("Indian_Tourism_ML_Big_Dataset.csv")

encoders = {}
for col in ["Weather","Crowd_Level","Tourism_Type","Budget_Level"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

X = df[["Weather","Crowd_Level","Tourism_Type","Budget_Level"]]
y = df["Place_Name"]

model = RandomForestClassifier(n_estimators=200)
model.fit(X, y)

def predict_place(data):
    return model.predict([data])[0]
    