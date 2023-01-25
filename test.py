import numpy as np
import joblib
from app import db, DTSchool
import pandas as pd

le = joblib.load('label_encoder.joblib')
model = joblib.load('school recommender.joblib')


course = input("Enter the course name: ")
tuition_fee = input("Enter the tuition fee: ")
location = input("Enter the location: ")
school_data = pd.read_sql_query(db.session.query(DTSchool).filter_by(Course=course).statement, db.session.bind)
for column_name in school_data.columns:
    if school_data[column_name].dtype == object:
        school_data[column_name] = le.fit_transform(school_data[column_name])
    else:
        pass
# Create a mapping dictionary that maps each possible course value to its corresponding index
course_mapping = {
    'Bachelor of Elementary Education': 0,
    'Bachelor of Science in Accountancy': 1,
    'Bachelor of Science in Architecture': 2,
    'Bachelor of Science in Civil Engineering': 3,
    'Bachelor of Science in Criminology': 4,
    'Bachelor of Science in Electrical Engineering': 5,
    'Bachelor of Science in Electronics Engineering': 6,
    'Bachelor of Science in Mechanical Engineering': 7,
    'Bachelor of Science in Nursing': 8,
    'Bachelor of Science in Psychology': 9,
    'Bachelor of Secondary Education': 10,
    'Bachelor of Secondary Education Major in English': 11,
    'Bachelor of Secondary Education Major in Filipino': 12,
    'Bachelor of Secondary Education Major in Mathematics': 13,
    'Bachelor of Secondary Education Major in Social Studies': 14
    # Add other possible course values and their indices here
}
tuition_mapping = {
    '0 - 20000': 0,
    '21000 - 40000': 1,
    '41000 - 60000': 2,
    'Free Tuition': 3,
    # Add other possible location values and their indices here
}

# Create a mapping dictionary that maps each possible location value to its corresponding index
location_mapping = {
    'Brgy. Bucal': 0,
    'Brgy. Halang': 1,
    'Brgy. III': 2,
    'Brgy. Makiling': 3,
    'Brgy. Paciano Rizal': 4,
    'Brgy. Parian': 5,
    'Brgy. VII': 6,
    # Add other possible location values and their indices here
}

encoded_input_values = [
    course_mapping[course],
    tuition_mapping[tuition_fee],
    location_mapping[location]
]
#
# predictions = model.predict([encoded_input_values])
# # le.fit_transform(predictions)
# print(le.inverse_transform(predictions))

# Make predictions on test data using the predict_proba method
probabilities = model.predict_proba([encoded_input_values])

# Get schools for each data point
schools = np.argsort(-probabilities, axis=1)[:, :9]
indices = np.where(
    (school_data['Course'] == course_mapping[course]) & (school_data['Tuition_Fee'] == tuition_mapping[tuition_fee]) | (
                school_data['Location'] == location_mapping[location]))

schools = schools[indices]
schools_flat = schools.flatten()


recommended_schools = le.inverse_transform(np.take(schools_flat, indices)).tolist()
print(recommended_schools)

indices = np.where(
    (school_data['Course'] == course_mapping[course]) & (school_data['Tuition_Fee'] == tuition_mapping[tuition_fee]) | (
                school_data['Location'] == location_mapping[location]))
filtered_schools = school_data.iloc[indices]['School'].tolist()
print(le.inverse_transform(filtered_schools))
