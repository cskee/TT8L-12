from flask import Flask,  redirect, url_for, render_template, request

app = Flask(__name__)

mmu_student = False

@app.route('/mmustudent/<name>')
def mmustudent(name):  
    return render_template("homepage.html",name=name,mmustudent=mmustudent)

@app.route("/notmmustudent/<name>")
def notmmustudent(name):
    return render_template("homepage.html",name=name)

@app.route("/2-handshop")
def secondhandshop():
    return render_template("2-handshop.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    global mmu_student
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if "@student.mmu.edu.my" in email:
            mmu_student = True
            username = email.split('@')[0]
            return redirect(url_for('mmustudent', name=username))
        else:
            mmu_student = False
            username = email.split('@')[0]
            return redirect(url_for('notmmustudent',name=username))
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)