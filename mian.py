from flask import Flask,  redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    else:
        return render_template("loginpage.html")

if __name__ == "__main__":
    app.run(debug=True)