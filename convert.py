# Import pandas and the School model
import pandas as pd
from app import db, ScProfiles

# Read the CSV file into a DataFrame
df = pd.read_csv('new-profile.csv', encoding='ISO-8859-1')

for _, row in df.iterrows():
    # Check if the record already exists in the database
    existing_record = ScProfiles.query.filter_by(School=row['School'], Location=row['Location'], City=row['City'],
                                                 Course=row['Course'], T_Range=row['TRange']).first()
    if existing_record:
        # Record already exists, skip the current iteration and move on to the next row
        continue

    # Create a new instance of the School model
    school = ScProfiles()

    # Set the attributes of the model to the values in the corresponding columns of the DataFrame
    school.School = row['School']
    school.Tuition_Fee = row['Tuition Fee']
    school.Location = row['Location']
    school.City = row['City']
    school.Course = row['Course']
    school.T_Range = row['TRange']

    # Add the instance to the database and commit the changes
    db.session.add(school)
    db.session.commit()
