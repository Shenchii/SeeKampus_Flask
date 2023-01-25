import numpy as np
import joblib
from app import db, DTSchool
import pandas as pd

le = joblib.load('label_encoder.joblib')
model = joblib.load('school recommender.joblib')

course = input("Enter the course name: ")
tuition_fee = input("Enter the tuition fee: ")
location = input("Enter the location: ")


sprofiles = pd.read_sql_query(db.session.query(DTSchool).filter_by(Course=course).statement,
                              db.session.bind)
indices = np.where(
    (sprofiles['Course'] == course) & (sprofiles['Tuition_Fee'] == tuition_fee) | (
            sprofiles['Location'] == location))
filtered_schools = sprofiles.iloc[indices]['School'].tolist()
print(filtered_schools)
