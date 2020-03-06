from flask import Flask, session, redirect, url_for, escape, request,render_template
app = Flask(__name__)

# app.secret_key = 'any random string’


@app.route('/')
def index():
    return render_template('template.html')


if __name__ == '__main__':
   app.run(debug = True)