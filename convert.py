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
    school.PR1_2023 = row['2023PR1']
    school.PR2_2023 = row['2023PR2']
    school.PR1_2024 = row['2024PR1']
    school.PR2_2024 = row['2024PR2']
    school.PR1_2025 = row['2025PR1']
    school.PR2_2025 = row['2025PR2']
    school.PR1_2026 = row['2026PR1']
    school.PR2_2026 = row['2026PR2']
    school.PR1_2027 = row['2027PR1']
    school.PR2_2027 = row['2027PR2']
    school.PR1_2028 = row['2028PR1']
    school.PR2_2028 = row['2028PR2']
    school.PR1_2029 = row['2029PR1']
    school.PR2_2029 = row['2029PR2']
    school.PR1_2030 = row['2030PR1']
    school.PR2_2030 = row['2030PR2']


    # Add the instance to the database and commit the changes
    db.session.add(school)
    db.session.commit()
