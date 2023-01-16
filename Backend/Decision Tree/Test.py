import numpy as np
import joblib


le = joblib.load('label_encoder.joblib')
model = joblib.load('school recommender.joblib')




course = input("Enter the course name: ")
tuition_fee = input("Enter the tuition fee: ")
location = input("Enter the location: ")


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


def recommended_schools_by_course(recommended_schools, course):
    # Create a list to store the schools that offer the inputed course
    schools_offering_course = []
    # Iterate through the recommended schools
    for school in recommended_schools:
        # Check if the school offers the inputed course
        if school_offers_course(school, course):
            # If the school does offer the inputed course, add it to the list
            schools_offering_course.append(school)
    # Return the list of schools that offer the inputed course
    return schools_offering_course


def school_offers_course(school, course):
    # check if the school offers the inputed course
    # replace this with a real implementation that checks the school's course offerings
    return True


encoded_input_values = [
    course_mapping[course],
    tuition_fee,
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

# Flatten the array
schools_flat = schools.flatten()


# Convert the integer labels back into the original string labels
recommended_schools = le.inverse_transform(schools_flat).tolist()


# filter the schools that are not offering the inputed course
final_recommendations = recommended_schools_by_course(recommended_schools, course)

print(final_recommendations)