# Import pandas and the School model
import pandas as pd
from app import db, ScProfiles

# Read the CSV file into a DataFrame
df = pd.read_csv('scprofile.csv')

# Iterate over the rows of the DataFrame
for _, row in df.iterrows():
    # Create a new instance of the School model
    school = ScProfiles()

    # Set the attributes of the model to the values in the corresponding columns of the DataFrame
    school.School = row['School']
    school.Tuition_Fee = row['Tuition Fee']
    school.Location = row['Location']
    school.City = row['City']
    school.Course = row['Course']



    # Add the instance to the database and commit the changes
    db.session.add(school)
    db.session.commit()
