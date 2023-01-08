from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('home.html')




if __name__ == '__main__':
    app.run()
