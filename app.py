from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register.html')
def home():
    return render_template('register.html')

@app.route('/login.html')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
