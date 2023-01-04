import joblib


le = joblib.load('label_encoder.joblib')
model = joblib.load('school recommender.joblib')

course = input("Enter the course name: ")
tuition_fee = input("Enter the tuition fee: ")
location = input("Enter the location: ")

# # # Find the column indices of the user-specified input values
# column_names = list(school_data.columns)
# course_index = column_names.index('Course')
# tuition_fee_index = column_names.index('Tuition Fee')
# location_index = column_names.index('Location')
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
# Create a mapping dictionary that maps each possible tuition fee value to its corresponding index
tuition_fee_mapping = {
    '12000': 0,
    '13000': 1,
    '14000': 2,
    '16000': 3,
    '17000': 4,
    '18000': 5,
    '19000': 6,
    '20000': 7,
    '21000': 8,
    '22000': 9,
    '23000': 10,
    '24000': 11,
    '25000': 12,
    '26000': 13,
    '32000': 14,
    '33000': 15,
    '34000': 16,
    '38000': 17,
    '40000': 18,
    '41000': 19,
    '42000': 20,
    '43000': 21,
    '44000': 22,
    '45000': 23,
    '46000': 24,
    '47000': 25,
    '48000': 26,
    '49000': 27,
    '50000': 28,
    '51000': 29,
    '52000': 30,
    '53000': 31,
    '54000': 32,
    '55000': 33,
    '56000': 34,
    '57000': 35,
    '58000': 36,
    '59000': 37,
    '60000': 38,
    '61000': 39,
    '62000': 40,
    '63000': 41,
    '64000': 42,
    '65000': 43,
    '70000': 44,
    '71000': 45,
    '72000': 46,
    '73000': 47,
    '74000': 48,
    '75000': 49,
    '76000': 50,
    '77000': 51,
    '78000': 52,
    '79000': 53,
    '80000': 54,
    '81000': 55,
    '82000': 56,
    '83000': 57,
    '84000': 58,
    '85000': 59,
    '86000': 60,
    '87000': 61,
    '88000': 62,
    '89000': 63,
    '90000': 64,
    # Add other possible tuition fee values and their indices here
}
# Create a mapping dictionary that maps each possible location value to its corresponding index
location_mapping = {
    'Brgy. Bucal': 0,
    'Brgy. Halang': 1,
    'Brgy. Makiling': 2,
    'Brgy. Paciano Rizal': 3,
    'Brgy. Parian': 4,
    'Brgy. Tres': 5,
    # Add other possible location values and their indices here
}

encoded_input_values = [
    course_mapping[course],
    tuition_fee_mapping[tuition_fee],
    location_mapping[location]
]
#
predictions = model.predict([encoded_input_values])
# le.fit_transform(predictions)
print(le.inverse_transform(predictions))
