from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import joblib
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SeeKampus.db'
db = SQLAlchemy(app)

le = joblib.load('label_encoder.joblib')


class DTSchool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Course = db.Column(db.String(255))
    Tuition_Fee = db.Column(db.String(255))
    Location = db.Column(db.String(255))
    School = db.Column(db.String(255))

    def __repr__(self):
        return '<DTSchool %r>' % self.id


class ScProfiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    School = db.Column(db.String(255))
    Tuition_Fee = db.Column(db.String(255))
    Location = db.Column(db.String(255))
    Course = db.Column(db.String(255))

    def __repr__(self):
        return '<ScProfiles %r>' % self.id


@app.route('/')
def index():  # put application's code here
    return render_template('home.html')


@app.route('/register', methods=['POST'])
def register():
    course = request.form['course']
    tuition_fee = request.form['tuition_fee']
    location = request.form['location']
    year = request.form['year']

    # Create a mapping dictionary that maps each possible course value to its corresponding index
    course_mapping = {
        'Bachelor of Elementary Education': 0,
        'Bachelor of Science in Accountancy': 0,
        'Bachelor of Science in Architecture': 0,
        'Bachelor of Science in Civil Engineering': 0,
        'Bachelor of Science in Criminology': 0,
        'Bachelor of Science in Electrical Engineering': 0,
        'Bachelor of Science in Electronics Engineering': 0,
        'Bachelor of Science in Mechanical Engineering': 0,
        'Bachelor of Science in Nursing': 0,
        'Bachelor of Science in Psychology': 0,
        'Bachelor of Secondary Education': 0,
        'Bachelor of Secondary Education Major in English': 0,
        'Bachelor of Secondary Education Major in Filipino': 0,
        'Bachelor of Secondary Education Major in Mathematics': 0,
        'Bachelor of Secondary Education Major in Social Studies': 0
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
    # Execute a query and store the results in a DataFrame
    school_data = pd.read_sql_query(db.session.query(DTSchool).filter_by(Course=course).statement, db.session.bind)

    for column_name in school_data.columns:
        if school_data[column_name].dtype == object:
            school_data[column_name] = le.fit_transform(school_data[column_name])
        else:
            pass

    X = school_data.drop(columns=['School', 'id'])
    y = school_data['School']

    dt_model = DecisionTreeClassifier()
    dt_model.fit(X, y)

    # Make predictions on test data using the predict_proba method
    probabilities = dt_model.predict_proba([encoded_input_values])
    # schools_offering_course = DTSchool.query.filter_by(Course=course).all()

    # Get schools for each data point
    schools = np.argsort(-probabilities, axis=1)[:, :9]

    # Flatten the array
    schools_flat = schools.flatten()

    # Convert the integer labels back into the original string labels
    recommended_schools = le.inverse_transform(schools_flat).tolist()
    recommended_schools = get_school_profiles(recommended_schools)
    return render_template('register.html', recommended_schools=recommended_schools)


def get_school_profiles(recommended_schools):
    school_profiles = []
    for school in recommended_schools:
        school_profile = ScProfiles.query.filter_by(School=school).first()
        if school_profile:
            school_profiles.append({
                'School': school_profile.School,
                'Tuition_Fee': school_profile.Tuition_Fee,
                'Location': school_profile.Location,
                'Course': school_profile.Course
            })
    return school_profiles


@app.route('/home')
def home():  # put application's code here
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
