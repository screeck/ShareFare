from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('templates/index.html')

@app.route('/register')
def register():
    return render_template('templates/register.html')

@app.route('/login')
def login():
    return render_template('templates/login.html')

@app.route('/main')
def main():
    return render_template('templates/main.html')

if __name__ == '__main__':
    app.run(debug=True)
