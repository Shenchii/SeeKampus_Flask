import math
import joblib
import os
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


class ScProfiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    School = db.Column(db.String(255))
    Tuition_Fee = db.Column(db.String(255))
    Location = db.Column(db.String(255))
    City = db.Column(db.String(255))
    Course = db.Column(db.String(255))
    T_Range = db.Column(db.String(255))

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


@app.route('/top-courses-batangas')
def top_courses_batangas():
    courses = ['Bachelor of Science in Elementary Education',
               'Bachelor of Science in Accountancy',
               'Bachelor of Science in Architecture',
               'Bachelor of Science in Civil Engineering',
               'Bachelor of Science in Criminology',
               'Bachelor of Science in Electrical Engineering',
               'Bachelor of Science in Electronics Engineering',
               'Bachelor of Science in Mechanical Engineering',
               'Bachelor of Science in Nursing',
               'Bachelor of Science in Psychology',
               'Bachelor of Science in Secondary Education']

    be_course = {
        'Bachelor of Science in Accountancy': 'hd-Accountancy.csv',
        'Bachelor of Science in Elementary Education': 'hd-Elementary Education.csv',
        'Bachelor of Science in Architecture': 'hd-Architecture.csv',
        'Bachelor of Science in Civil Engineering': 'hd-Civil Engineering.csv',
        'Bachelor of Science in Criminology': 'hd-Criminology.csv',
        'Bachelor of Science in Electrical Engineering': 'hd-Electrical Engineering.csv',
        'Bachelor of Science in Electronics Engineering': 'hd-Electronics Engineering.csv',
        'Bachelor of Science in Mechanical Engineering': 'hd-Mechanical Engineering.csv',
        'Bachelor of Science in Nursing': 'hd-Nursing.csv',
        'Bachelor of Science in Psychology': 'hd-Psychology.csv',
        'Bachelor of Science in Secondary Education': 'hd-Secondary Education.csv'
    }

    location = 'Batangas'
    school_data = pd.read_sql_query(db.session.query(ScProfiles).filter(
        (ScProfiles.Location == location)
    ).statement, db.session.bind)

    schools = school_data['School']

    results = {}
    for course in courses:
        df = pd.read_csv(f'Historical Data/{be_course[course]}', encoding='windows-1252')
        df_school = df[df['School'].astype(str).isin(schools)]
        df_school['Passing Rate'] = pd.to_numeric(df_school['Passing Rate'], errors='coerce')
        avg_passing_rate = round(df_school['Passing Rate'].mean(), 2)
        results[course] = avg_passing_rate

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    sorted_list = []
    for i, (course, passing_rate) in enumerate(sorted_results, start=1):
        sorted_list.append({'rank': i, 'course': course, 'passing_rate': passing_rate})

    return render_template('top-courses-batangas.html', results=sorted_list)


@app.route('/top-courses-cavite')
def top_courses_cavite():
    courses = ['Bachelor of Science in Elementary Education',
               'Bachelor of Science in Accountancy',
               'Bachelor of Science in Architecture',
               'Bachelor of Science in Civil Engineering',
               'Bachelor of Science in Criminology',
               'Bachelor of Science in Electrical Engineering',
               'Bachelor of Science in Electronics Engineering',
               'Bachelor of Science in Mechanical Engineering',
               'Bachelor of Science in Nursing',
               'Bachelor of Science in Psychology',
               'Bachelor of Science in Secondary Education']

    be_course = {
        'Bachelor of Science in Accountancy': 'hd-Accountancy.csv',
        'Bachelor of Science in Elementary Education': 'hd-Elementary Education.csv',
        'Bachelor of Science in Architecture': 'hd-Architecture.csv',
        'Bachelor of Science in Civil Engineering': 'hd-Civil Engineering.csv',
        'Bachelor of Science in Criminology': 'hd-Criminology.csv',
        'Bachelor of Science in Electrical Engineering': 'hd-Electrical Engineering.csv',
        'Bachelor of Science in Electronics Engineering': 'hd-Electronics Engineering.csv',
        'Bachelor of Science in Mechanical Engineering': 'hd-Mechanical Engineering.csv',
        'Bachelor of Science in Nursing': 'hd-Nursing.csv',
        'Bachelor of Science in Psychology': 'hd-Psychology.csv',
        'Bachelor of Science in Secondary Education': 'hd-Secondary Education.csv'
    }

    location = 'Cavite'
    school_data = pd.read_sql_query(db.session.query(ScProfiles).filter(
        (ScProfiles.Location == location)
    ).statement, db.session.bind)

    schools = school_data['School']

    results = {}
    for course in courses:
        df = pd.read_csv(f'Historical Data/{be_course[course]}', encoding='windows-1252')
        df_school = df[df['School'].astype(str).isin(schools)]
        df_school['Passing Rate'] = pd.to_numeric(df_school['Passing Rate'], errors='coerce')
        avg_passing_rate = round(df_school['Passing Rate'].mean(), 2)
        results[course] = avg_passing_rate

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    sorted_list = []
    for i, (course, passing_rate) in enumerate(sorted_results, start=1):
        sorted_list.append({'rank': i, 'course': course, 'passing_rate': passing_rate})
    return render_template('top-courses-cavite.html', results=sorted_list)


@app.route('/top-courses-laguna')
def top_courses_laguna():
    courses = ['Bachelor of Science in Elementary Education',
               'Bachelor of Science in Accountancy',
               'Bachelor of Science in Architecture',
               'Bachelor of Science in Civil Engineering',
               'Bachelor of Science in Criminology',
               'Bachelor of Science in Electrical Engineering',
               'Bachelor of Science in Electronics Engineering',
               'Bachelor of Science in Mechanical Engineering',
               'Bachelor of Science in Nursing',
               'Bachelor of Science in Psychology',
               'Bachelor of Science in Secondary Education']

    be_course = {
        'Bachelor of Science in Accountancy': 'hd-Accountancy.csv',
        'Bachelor of Science in Elementary Education': 'hd-Elementary Education.csv',
        'Bachelor of Science in Architecture': 'hd-Architecture.csv',
        'Bachelor of Science in Civil Engineering': 'hd-Civil Engineering.csv',
        'Bachelor of Science in Criminology': 'hd-Criminology.csv',
        'Bachelor of Science in Electrical Engineering': 'hd-Electrical Engineering.csv',
        'Bachelor of Science in Electronics Engineering': 'hd-Electronics Engineering.csv',
        'Bachelor of Science in Mechanical Engineering': 'hd-Mechanical Engineering.csv',
        'Bachelor of Science in Nursing': 'hd-Nursing.csv',
        'Bachelor of Science in Psychology': 'hd-Psychology.csv',
        'Bachelor of Science in Secondary Education': 'hd-Secondary Education.csv'
    }

    location = 'Laguna'
    school_data = pd.read_sql_query(db.session.query(ScProfiles).filter(
        (ScProfiles.Location == location)
    ).statement, db.session.bind)

    schools = school_data['School']

    results = {}
    for course in courses:
        df = pd.read_csv(f'Historical Data/{be_course[course]}', encoding='windows-1252')
        df_school = df[df['School'].astype(str).isin(schools)]
        df_school['Passing Rate'] = pd.to_numeric(df_school['Passing Rate'], errors='coerce')
        avg_passing_rate = round(df_school['Passing Rate'].mean(), 2)
        results[course] = avg_passing_rate

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    sorted_list = []
    for i, (course, passing_rate) in enumerate(sorted_results, start=1):
        sorted_list.append({'rank': i, 'course': course, 'passing_rate': passing_rate})
    return render_template('top-courses-laguna.html', results=sorted_list)


@app.route('/top-courses-ncr')
def top_courses_ncr():
    courses = ['Bachelor of Science in Elementary Education',
               'Bachelor of Science in Accountancy',
               'Bachelor of Science in Architecture',
               'Bachelor of Science in Civil Engineering',
               'Bachelor of Science in Criminology',
               'Bachelor of Science in Electrical Engineering',
               'Bachelor of Science in Electronics Engineering',
               'Bachelor of Science in Mechanical Engineering',
               'Bachelor of Science in Nursing',
               'Bachelor of Science in Psychology',
               'Bachelor of Science in Secondary Education']

    be_course = {
        'Bachelor of Science in Accountancy': 'hd-Accountancy.csv',
        'Bachelor of Science in Elementary Education': 'hd-Elementary Education.csv',
        'Bachelor of Science in Architecture': 'hd-Architecture.csv',
        'Bachelor of Science in Civil Engineering': 'hd-Civil Engineering.csv',
        'Bachelor of Science in Criminology': 'hd-Criminology.csv',
        'Bachelor of Science in Electrical Engineering': 'hd-Electrical Engineering.csv',
        'Bachelor of Science in Electronics Engineering': 'hd-Electronics Engineering.csv',
        'Bachelor of Science in Mechanical Engineering': 'hd-Mechanical Engineering.csv',
        'Bachelor of Science in Nursing': 'hd-Nursing.csv',
        'Bachelor of Science in Psychology': 'hd-Psychology.csv',
        'Bachelor of Science in Secondary Education': 'hd-Secondary Education.csv'
    }

    location = 'NCR'
    school_data = pd.read_sql_query(db.session.query(ScProfiles).filter(
        (ScProfiles.Location == location)
    ).statement, db.session.bind)

    schools = school_data['School']

    results = {}
    for course in courses:
        df = pd.read_csv(f'Historical Data/{be_course[course]}', encoding='windows-1252')
        df_school = df[df['School'].astype(str).isin(schools)]
        df_school['Passing Rate'] = pd.to_numeric(df_school['Passing Rate'], errors='coerce')
        avg_passing_rate = round(df_school['Passing Rate'].mean(), 2)
        results[course] = avg_passing_rate

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    sorted_list = []
    for i, (course, passing_rate) in enumerate(sorted_results, start=1):
        sorted_list.append({'rank': i, 'course': course, 'passing_rate': passing_rate})
    return render_template('top-courses-ncr.html', results=sorted_list)


@app.route('/top-courses-quezon')
def top_courses_quezon():
    courses = ['Bachelor of Science in Elementary Education',
               'Bachelor of Science in Accountancy',
               'Bachelor of Science in Architecture',
               'Bachelor of Science in Civil Engineering',
               'Bachelor of Science in Criminology',
               'Bachelor of Science in Electrical Engineering',
               'Bachelor of Science in Electronics Engineering',
               'Bachelor of Science in Mechanical Engineering',
               'Bachelor of Science in Nursing',
               'Bachelor of Science in Psychology',
               'Bachelor of Science in Secondary Education']

    be_course = {
        'Bachelor of Science in Accountancy': 'hd-Accountancy.csv',
        'Bachelor of Science in Elementary Education': 'hd-Elementary Education.csv',
        'Bachelor of Science in Architecture': 'hd-Architecture.csv',
        'Bachelor of Science in Civil Engineering': 'hd-Civil Engineering.csv',
        'Bachelor of Science in Criminology': 'hd-Criminology.csv',
        'Bachelor of Science in Electrical Engineering': 'hd-Electrical Engineering.csv',
        'Bachelor of Science in Electronics Engineering': 'hd-Electronics Engineering.csv',
        'Bachelor of Science in Mechanical Engineering': 'hd-Mechanical Engineering.csv',
        'Bachelor of Science in Nursing': 'hd-Nursing.csv',
        'Bachelor of Science in Psychology': 'hd-Psychology.csv',
        'Bachelor of Science in Secondary Education': 'hd-Secondary Education.csv'
    }

    location = 'Quezon Province'
    school_data = pd.read_sql_query(db.session.query(ScProfiles).filter(
        (ScProfiles.Location == location)
    ).statement, db.session.bind)

    schools = school_data['School']

    results = {}
    for course in courses:
        df = pd.read_csv(f'Historical Data/{be_course[course]}', encoding='windows-1252')
        df_school = df[df['School'].astype(str).isin(schools)]
        df_school['Passing Rate'] = pd.to_numeric(df_school['Passing Rate'], errors='coerce')
        avg_passing_rate = round(df_school['Passing Rate'].mean(), 2)
        results[course] = avg_passing_rate

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    sorted_list = []
    for i, (course, passing_rate) in enumerate(sorted_results, start=1):
        sorted_list.append({'rank': i, 'course': course, 'passing_rate': passing_rate})
    return render_template('top-courses-quezon.html', results=sorted_list)


@app.route('/top-courses-rizal')
def top_courses_rizal():
    courses = ['Bachelor of Science in Elementary Education',
               'Bachelor of Science in Accountancy',
               'Bachelor of Science in Architecture',
               'Bachelor of Science in Civil Engineering',
               'Bachelor of Science in Criminology',
               'Bachelor of Science in Electrical Engineering',
               'Bachelor of Science in Electronics Engineering',
               'Bachelor of Science in Mechanical Engineering',
               'Bachelor of Science in Nursing',
               'Bachelor of Science in Psychology',
               'Bachelor of Science in Secondary Education']

    be_course = {
        'Bachelor of Science in Accountancy': 'hd-Accountancy.csv',
        'Bachelor of Science in Elementary Education': 'hd-Elementary Education.csv',
        'Bachelor of Science in Architecture': 'hd-Architecture.csv',
        'Bachelor of Science in Civil Engineering': 'hd-Civil Engineering.csv',
        'Bachelor of Science in Criminology': 'hd-Criminology.csv',
        'Bachelor of Science in Electrical Engineering': 'hd-Electrical Engineering.csv',
        'Bachelor of Science in Electronics Engineering': 'hd-Electronics Engineering.csv',
        'Bachelor of Science in Mechanical Engineering': 'hd-Mechanical Engineering.csv',
        'Bachelor of Science in Nursing': 'hd-Nursing.csv',
        'Bachelor of Science in Psychology': 'hd-Psychology.csv',
        'Bachelor of Science in Secondary Education': 'hd-Secondary Education.csv'
    }

    location = 'Rizal'
    school_data = pd.read_sql_query(db.session.query(ScProfiles).filter(
        (ScProfiles.Location == location)
    ).statement, db.session.bind)

    schools = school_data['School']

    results = {}
    for course in courses:
        df = pd.read_csv(f'Historical Data/{be_course[course]}', encoding='windows-1252')
        df_school = df[df['School'].astype(str).isin(schools)]
        df_school['Passing Rate'] = pd.to_numeric(df_school['Passing Rate'], errors='coerce')
        avg_passing_rate = round(df_school['Passing Rate'].mean(), 2)
        if not np.isnan(avg_passing_rate):
            results[course] = avg_passing_rate

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    sorted_list = []
    for i, (course, passing_rate) in enumerate(sorted_results, start=1):
        sorted_list.append({'rank': i, 'course': course, 'passing_rate': passing_rate})
    return render_template('top-courses-rizal.html', results=sorted_list)


@app.route('/recommended-schools')
def another():
    return redirect(url_for('/recommended-schools'))


@app.route('/recommended-schools', methods=['POST'])
def register():
    course = request.form['course']
    tuition_fee = request.form['tuition_fee']
    location = request.form['location']
    be_course = {
        'Bachelor of Science in Accountancy': 'hd-Accountancy.csv',
        'Bachelor of Science in Elementary Education': 'hd-Elementary Education.csv',
        'Bachelor of Science in Architecture': 'hd-Architecture.csv',
        'Bachelor of Science in Civil Engineering': 'hd-Civil Engineering.csv',
        'Bachelor of Science in Criminology': 'hd-Criminology.csv',
        'Bachelor of Science in Electrical Engineering': 'hd-Electrical Engineering.csv',
        'Bachelor of Science in Electronics Engineering': 'hd-Electronics Engineering.csv',
        'Bachelor of Science in Mechanical Engineering': 'hd-Mechanical Engineering.csv',
        'Bachelor of Science in Nursing': 'hd-Nursing.csv',
        'Bachelor of Science in Psychology': 'hd-Psychology.csv',
        'Bachelor of Science in Secondary Education': 'hd-Secondary Education.csv',
        'Bachelor of Science in Secondary Education Major in English': 'hd-Secondary Education.csv',
        'Bachelor of Science in Secondary Education Major in Filipino': 'hd-Secondary Education.csv',
        'Bachelor of Science in Secondary Education Major in Mathematics': 'hd-Secondary Education.csv',
        'Bachelor of Science in Secondary Education Major in Social Studies': 'hd-Secondary Education.csv'
    }

    # Create a mapping dictionary that maps each possible course value to its corresponding index
    course_mapping = {
        'Bachelor of Science in Elementary Education': 0,
        'Bachelor of Science in Accountancy': 0,
        'Bachelor of Science in Architecture': 0,
        'Bachelor of Science in Civil Engineering': 0,
        'Bachelor of Science in Criminology': 0,
        'Bachelor of Science in Electrical Engineering': 0,
        'Bachelor of Science in Electronics Engineering': 0,
        'Bachelor of Science in Mechanical Engineering': 0,
        'Bachelor of Science in Nursing': 0,
        'Bachelor of Science in Psychology': 0,
        'Bachelor of Science in Secondary Education': 0,
        'Bachelor of Science in Secondary Education Major in English': 0,
        'Bachelor of Science in Secondary Education Major in Filipino': 0,
        'Bachelor of Science in Secondary Education Major in Mathematics': 0,
        'Bachelor of Science in Secondary Education Major in Social Studies': 0
        # Add other possible course values and their indices here
    }
    tuition_mapping = {
        '0 - 20000': 0,
        '21000 - 40000': 1,
        '41000 - 60000': 2,
        '61000 - 80000': 3,
        '81000 - 100000': 4,
        '101000 - 120000': 5,
        '150000 above': 6,
        'Free Tuition': 7,
        # Add other possible location values and their indices here
    }

    # Create a mapping dictionary that maps each possible location value to its corresponding index
    location_mapping = {
        'Laguna': 0,
        'Cavite': 1,
        'Batangas': 2,
        'Rizal': 3,
        'Quezon Province': 4,
        'NCR': 5,
        'Any': 6,
        # Add other possible location values and their indices here
    }
    encoded_input_values = [
        course_mapping[course],
        tuition_mapping[tuition_fee],
        location_mapping[location]
    ]
    # Execute a query and store the results in a DataFrame
    school_data = pd.read_sql_query(db.session.query(ScProfiles).filter_by(Course=course).statement, db.session.bind)

    for column_name in school_data.columns:
        if school_data[column_name].dtype == object:
            school_data[column_name] = le.fit_transform(school_data[column_name])
        else:
            pass

    X = school_data.drop(columns=['School', 'id', 'City', 'Tuition_Fee'])
    y = school_data['School']

    dt_model = DecisionTreeClassifier()
    dt_model.fit(X, y)

    # Make predictions on test data using the predict_proba method
    probabilities = dt_model.predict_proba([encoded_input_values])

    # Get schools for each data point
    schools = np.argsort(-probabilities, axis=1)[:, :9]

    # Flatten the array
    schools_flat = schools.flatten()
    if location == 'Any':
        school_data = pd.read_sql_query(db.session.query(ScProfiles).filter(
            (ScProfiles.Course == course) & (ScProfiles.T_Range == tuition_fee)
        ).statement, db.session.bind)
    else:
        school_data = pd.read_sql_query(db.session.query(ScProfiles).filter(
            (ScProfiles.Course == course) & (ScProfiles.T_Range == tuition_fee) & (ScProfiles.Location == location)
        ).statement, db.session.bind)

    # Convert the integer labels back into the original string labels
    schools = school_data['School'].tolist()
    df = pd.read_csv(f'Historical Data/{be_course[course]}', encoding='windows-1252')

    df['Year'] = df['Time Date'].apply(lambda x: str(x)[-4:])
    df['Month'] = df['Time Date'].apply(lambda x: str(x)[-6:-4])
    df['Day'] = df['Time Date'].apply(lambda x: str(x)[:-6])
    df['ds'] = pd.DatetimeIndex(df['Year'] + '-' + df['Month'] + '-' + df['Day'])
    all_yhat_values = []
    for school in schools:
        df_school = df[df['School'] == school]
        df_school.drop(['Time Date', 'School', 'Course', 'Year', 'Month', 'Day'], axis=1, inplace=True)
        df_school.columns = ['y', 'ds']

        # Check if there are at least two non-NaN rows
        if df_school.dropna().shape[0] >= 2:
            # Create a Prophet model
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
        else:
            all_yhat_values.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

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
        school_profile = ScProfiles.query.filter_by(School=school).first()
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
            return redirect(url_for('upload'))
        else:
            flash('You are not an admin')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
@login_required
def upload_post():
    course = request.form['course']
    year = request.form['year']
    batch = request.form['batch']
    file = request.files['file']
    batch_dates = {
        'a': f'3012{year}',
        'b': f'3112{year}',
    }
    if not file:
        return "No file"

    if not file.filename.endswith('.csv'):

        return redirect(url_for('upload'))

    filename = f"{course}-{year}{batch}.csv"
    file_path = os.path.join(f'Historical Data/Yearly/{course}/{course}-{year}{batch}.csv')
    file.save(file_path)
    # read test.csv into a pandas dataframe
    test = pd.read_csv(f'Historical Data/Yearly/{course}/{course}-{year}{batch}.csv', header=0, encoding='windows-1252')

    # rename the columns in test dataframe
    test.columns = ['School', 'Passing Rate']
    test['School'] = test['School'].str.replace('\n', ' ').str.replace('-', '')
    test['Passing Rate'] = test['Passing Rate'].str.replace('%', '')
    test.dropna(inplace=True)
    # add a new column 'Course' to test dataframe and fill with 'Bachelor of Science in Accountancy'
    test['Course'] = f'Bachelor of Science in {course}'

    # add a new column 'Time Date' to test dataframe and fill with '30122010'
    test['Time Date'] = batch_dates[batch]

    # read hd_course csv into a pandas dataframe
    hd_course = pd.read_csv(f'Historical Data/hd-{course}.csv', header=0, encoding='windows-1252')

    # concatenate the two dataframes along axis 0 (row-wise)
    result = pd.concat([hd_course, test], axis=0)

    result.drop_duplicates(inplace=True)  # removes duplicate rows
    # result.dropna(inplace=True)  # removes rows with missing values

    result = result.sort_values(by='School', ascending=True)

    # write the result dataframe to a new csv file
    result.to_csv(f'Historical Data/hd-{course}.csv', index=False, encoding='windows-1252')

    return redirect(url_for('uploaded'))


@app.route('/uploaded')
@login_required
def uploaded():
    return render_template('uploaded.html')


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
