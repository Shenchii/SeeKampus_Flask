# Import pandas and the School model
import pandas as pd
from app import db, dt_School

# Read the CSV file into a DataFrame
df = pd.read_csv('school profiles.csv')

# Iterate over the rows of the DataFrame
for _, row in df.iterrows():
    # Create a new instance of the School model
    school = dt_School()

    # Set the attributes of the model to the values in the corresponding columns of the DataFrame
    school.Course = row['Course']
    school.Tuition_Fee = row['Tuition Fee']
    school.Location = row['Location']
    school.School = row['School']

    # Add the instance to the database and commit the changes
    db.session.add(school)
    db.session.commit()
