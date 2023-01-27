import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sklearn.tree import DecisionTreeClassifier
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SeeKampus.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

admin = Admin(app, name='SeeKampus', template_mode='bootstrap3')

le = joblib.load('label_encoder.joblib')
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class AdminAccount(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(255))

    def __repr__(self):
        return '<User %r>' % self.id


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
    PR1_2023 = db.Column(db.String(255))
    PR2_2023 = db.Column(db.String(255))
    PR1_2024 = db.Column(db.String(255))
    PR2_2024 = db.Column(db.String(255))
    PR1_2025 = db.Column(db.String(255))
    PR2_2025 = db.Column(db.String(255))
    PR1_2026 = db.Column(db.String(255))
    PR2_2026 = db.Column(db.String(255))
    PR1_2027 = db.Column(db.String(255))
    PR2_2027 = db.Column(db.String(255))
    PR1_2028 = db.Column(db.String(255))
    PR2_2028 = db.Column(db.String(255))
    PR1_2029 = db.Column(db.String(255))
    PR2_2029 = db.Column(db.String(255))
    PR1_2030 = db.Column(db.String(255))
    PR2_2030 = db.Column(db.String(255))

    def __repr__(self):
        return '<ScProfiles %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return AdminAccount.query.get(int(user_id))


admin.add_view(ModelView(ScProfiles, db.session))


@app.route('/')
def index():  # put application's code here
    return render_template('home.html')


@app.route('/register')
def another():
    return redirect(url_for('/home'))


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

    # Get schools for each data point
    schools = np.argsort(-probabilities, axis=1)[:, :9]

    # Flatten the array
    schools_flat = schools.flatten()

    school_data = pd.read_sql_query(db.session.query(DTSchool).filter(
    (DTSchool.Course == course) & (DTSchool.Tuition_Fee == tuition_fee) | (DTSchool.Location == location)
    ).statement, db.session.bind)


    # Convert the integer labels back into the original string labels
    recommended_schools = school_data['School']
    recommended_schools = get_school_profiles(recommended_schools, year)
    return render_template('register.html', recommended_schools=recommended_schools, year=year, course=course,
                           tuition_fee=tuition_fee, location=location)


def get_school_profiles(recommended_schools, year):
    school_profiles = []
    for school in recommended_schools:
        school_profile = ScProfiles.query.filter_by(School=school).first()
        if school_profile:
            pr1_column = 'PR1_' + year
            school_profiles.append({
                'School': school_profile.School,
                'Tuition_Fee': school_profile.Tuition_Fee,
                'Location': school_profile.Location,
                'Course': school_profile.Course,
                'PR1': getattr(school_profile, pr1_column)
            })

    # Sort the schools by PR1, with 'Insufficient Data' at the bottom
    school_profiles = sorted(school_profiles, key=lambda x: 0 if x['PR1'] == 'Insufficient Data' else int(x['PR1']),
                             reverse=True)

    return school_profiles


@app.route('/home')
def home():  # put application's code here
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

        user = AdminAccount.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))

        login_user(user, remember=remember)

        if current_user.role == 'admin':
            return redirect(url_for('admin.index'))
        else:
            flash('You are not an admin')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def create_admin():
    admin_exist = AdminAccount.query.filter_by(username='admin').first()
    if not admin_exist:
        admin1 = AdminAccount(username='admin', email='admin@example.com', password=generate_password_hash('password'),
                              role='admin')
        db.session.add(admin1)
        db.session.commit()


if __name__ == '__main__':
    create_admin()
    app.run(debug=True)
