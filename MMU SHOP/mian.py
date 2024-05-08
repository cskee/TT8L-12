from flask import Flask,  redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/homepage')
def homepage():
    return render_template("homepage.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return redirect(url_for('homepage'))
    else:
        return render_template("loginpage.html")

if __name__ == "__main__":
    app.run(debug=True)