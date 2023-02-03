import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user, login_required
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sklearn.tree import DecisionTreeClassifier
import prophet as Prophet
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


class MyView(AdminIndexView):
    def __init__(self, name, endpoint, **kwargs):
        super(MyView, self).__init__(name, endpoint, **kwargs)
        self.template_mode = 'my_template'

    def index(self):
        return render_template("admin.html")


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
    City = db.Column(db.String(255))
    School = db.Column(db.String(255))

    def __repr__(self):
        return '<DTSchool %r>' % self.id


class ScProfiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    School = db.Column(db.String(255))
    Tuition_Fee = db.Column(db.String(255))
    Location = db.Column(db.String(255))
    City = db.Column(db.String(255))
    Course = db.Column(db.String(255))

    def __repr__(self):
        return '<ScProfiles %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return AdminAccount.query.get(int(user_id))


admin.add_view(ModelView(ScProfiles, db.session))


# @app.route('/upload', methods=['POST'])
# def upload_file():
#     file = request.files['file']
#     if file.filename.endswith('.csv'):
#         df = pd.read_csv(file)
#         # do something with the dataframe, e.g. store it in a database
#         return "CSV file uploaded and processed."
#     return "Invalid file type. Please upload a CSV file."


@app.route('/')
def index():  # put application's code here
    return render_template('home.html')


@app.route('/recommend-by-school')
def recommend_by_school():
    return render_template('recommend-by-school.html')


@app.route('/recommended-schools')
def another():
    return redirect(url_for('/recommended-schools'))


@app.route('/recommended-schools', methods=['POST'])
def register():
    course = request.form['course']
    tuition_fee = request.form['tuition_fee']
    location = request.form['location']
    be_course = {
        'Bachelor of Science in Accountancy': 'hd-accountancy.csv',
        'Bachelor of Elementary Education': 'hd-EED.csv',
        'Bachelor of Science in Architecture': 'hd-Archi.csv',
        'Bachelor of Science in Civil Engineering': 'hd-Civil.csv',
        'Bachelor of Science in Criminology': 'hd-Crim.csv',
        'Bachelor of Science in Electrical Engineering': 'hd-Electrical.csv',
        'Bachelor of Science in Electronics Engineering': 'hd-Electronics.csv',
        'Bachelor of Science in Mechanical Engineering': 'hd-Mechanical.csv',
        'Bachelor of Science in Nursing': 'hd-Nursing.csv',
        'Bachelor of Science in Psychology': 'hd-Psychology.csv',
        'Bachelor of Secondary Education': 'hd-SED.csv',
        'Bachelor of Secondary Education Major in English': 'hd-SED.csv',
        'Bachelor of Secondary Education Major in Filipino': 'hd-SED.csv',
        'Bachelor of Secondary Education Major in Mathematics': 'hd-SED.csv',
        'Bachelor of Secondary Education Major in Social Studies': 'hd-SED.csv'
    }

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
        'Laguna': 0,
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

    X = school_data.drop(columns=['School', 'id', 'City'])
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
        (DTSchool.Course == course) & (DTSchool.Tuition_Fee == tuition_fee) & (DTSchool.Location == location)
    ).statement, db.session.bind)

    # Convert the integer labels back into the original string labels
    schools = school_data['School'].tolist()
    df = pd.read_csv(be_course[course])

    df['Year'] = df['Time Date'].apply(lambda x: str(x)[-4:])
    df['Month'] = df['Time Date'].apply(lambda x: str(x)[-6:-4])
    df['Day'] = df['Time Date'].apply(lambda x: str(x)[:-6])
    df['ds'] = pd.DatetimeIndex(df['Year'] + '-' + df['Month'] + '-' + df['Day'])
    all_yhat_values = []
    for school in schools:
        df_school = df[df['School'] == school]
        df_school.drop(['Time Date', 'School', 'Course', 'Year', 'Month', 'Day'], axis=1, inplace=True)
        df_school.columns = ['y', 'ds']

        m = Prophet.Prophet(interval_width=0.95)
        m.add_seasonality(name='yearly', period=365.25, fourier_order=10)
        m.add_seasonality(name='semi-annual', period=365.25 / 2, fourier_order=10)
        _model = m.fit(df_school)

        # Get the latest date in the original data frame
        latest_date = df_school['ds'].max()

        # Get the range of dates for the future data frame
        start_date = latest_date - pd.DateOffset(years=5)
        end_date = latest_date + pd.DateOffset(years=1)
        future_dates = pd.date_range(start_date, end_date, freq='Y')

        # Create the future data frame
        _future = pd.DataFrame({'ds': future_dates})

        # Get predictions for those specific dates
        _forecast = m.predict(_future)
        _forecast['yhat'] = _forecast['yhat'].clip(lower=0, upper=100).round()
        yhat_values = _forecast['yhat'].tolist()
        all_yhat_values.append(yhat_values)

    recommended_schools = get_school_profiles(schools, all_yhat_values)
    if not recommended_schools:
        return redirect(url_for('no_schools'))
    else:
        return render_template('recommended-schools.html', recommended_schools=recommended_schools, course=course,
                               be_course=be_course, schools=schools,
                               tuition_fee=tuition_fee, location=location, all_yhat_values=all_yhat_values)


def get_school_profiles(schools, all_yhat_values):
    school_profiles = []
    for i, school in enumerate(schools):
        school_profile = DTSchool.query.filter_by(School=school).first()
        if school_profile:
            school_profiles.append({
                'School': school_profile.School,
                'Tuition_Fee': school_profile.Tuition_Fee,
                'City': school_profile.City,
                'yhat_values': all_yhat_values[i]
            })

    return school_profiles


@app.route('/no_schools')
def no_schools():
    return render_template('no_school_found.html')


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
    session.clear()
    return redirect(url_for('login'))


def create_admin():
    admin_exist = AdminAccount.query.filter_by(username='admin').first()
    if not admin_exist:
        admin1 = AdminAccount(username='admin', email='admin@example.com', password=generate_password_hash('123'),
                              role='admin')
        db.session.add(admin1)
        db.session.commit()


if __name__ == '__main__':
    create_admin()
    app.run(debug=True)
