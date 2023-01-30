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
    school.Course = row['Course']
    school.PR_2023 = row['PR_2023']
    school.PR_2024 = row['PR_2024']
    school.PR_2025 = row['PR_2025']
    school.PR_2026 = row['PR_2026']
    school.PR_2027 = row['PR_2027']
    school.PR_2028 = row['PR_2028']
    school.PR_2029 = row['PR_2029']
    school.PR_2030 = row['PR_2030']


    # Add the instance to the database and commit the changes
    db.session.add(school)
    db.session.commit()
