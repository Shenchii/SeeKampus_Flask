from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import joblib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SeeKampus.db'
db = SQLAlchemy(app)

le = joblib.load('label_encoder.joblib')
dt_model = joblib.load('school recommender.joblib')


class DTSchool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Course = db.Column(db.String(255))
    Tuition_Fee = db.Column(db.Float)
    Location = db.Column(db.String(255))
    School = db.Column(db.String(255))

    def __repr__(self):
        return '<dt_School %r>' % self.id


@app.route('/')
def index():  # put application's code here
    return render_template('home.html')


@app.route('/register', methods=['POST'])
def register():
    course = request.form['course']
    tuition_fee = request.form['tuition']
    location = request.form['location']

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
    encoded_input_values = [
        course_mapping[course],
        tuition_fee,
        location_mapping[location]
    ]
    # Make predictions on test data using the predict_proba method
    probabilities = dt_model.predict_proba([encoded_input_values])

    # Get the top 3 classes (schools) for each data point
    top_5 = np.argsort(-probabilities, axis=1)[:, :5]

    # Flatten the array
    top_5_flat = top_5.flatten()

    # Convert the integer labels back into the original string labels
    recommended_schools = le.inverse_transform(top_5_flat).tolist()

    return render_template('register.html', schools=recommended_schools)


@app.route('/home')
def home():  # put application's code here
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
