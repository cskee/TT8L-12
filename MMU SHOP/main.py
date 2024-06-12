from flask import Flask,  redirect, url_for, render_template, request, make_response
import os

app = Flask(__name__)

mmu_student = False

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def write_data(product):
    with open('product.txt', 'a') as file:
        file.write(f"{product['product_name']},{product['price']},{product['type']},{product['image']}\n")
    
    if product['type'] == '2-handshop':
        with open('2_handshop_products.txt', 'a') as file:
            file.write(f"{product['product_name']},{product['price']},{product['type']},{product['image']}\n")

def delete_data(product):
    with open('product.txt', 'r') as file:
        lines = file.readlines()

    with open('product.txt', 'w') as file: 
        for line in lines:
            parts = line.strip().split(',')
            if parts[0] != product['product_name']:
                file.write(line)
        

def read_data():
    products = []
    with open('product.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4:
                product_name, price, p_type, image = parts
                products.append({'product_name': product_name, 'price': price, 'type': p_type, 'image': image})

    with open('2_handshop_products.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4:
                product_name, price, p_type, image = parts
                products.append({'product_name': product_name, 'price': price, 'type': p_type, 'image': image})

    return products




@app.route('/uploadproduct/<name>')
def uploadproduct(name):
    return render_template("sellerform.html",name=name,mmustudent=mmustudent)

@app.route('/notuploadproduct/<name>')
def notuploadproduct(name):
    return render_template("sellerform.html",name=name)


@app.route("/product", methods=['POST', 'GET'])
def product():
    name = request.form.get('name')
    if 'delete' in request.form:
        product_name_to_delete = request.form['delete']
        delete_data({'product_name': product_name_to_delete})
        if mmu_student:
            return redirect(url_for('mmustudent', name=name))
        else:
            return redirect(url_for('notmmustudent', name=name))
    else:
        if request.method == 'POST':
            if 'image' not in request.files:
                return redirect(request.url)
            file = request.files['image']
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                try:
                    filename = file.filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    new_product = {
                        'product_name': request.form['product_name'],
                        'price': request.form['price'],
                        'type': request.form['type'],
                        'image': filename
                    }
                    write_data(new_product)

                    if new_product['type'] == '2-handshop':
                        if mmu_student:
                            return redirect(url_for('secondhandshop', name=name)) 
                        else:
                            return redirect(url_for('notsecondhandshop', name=name))

                except Exception as e:
                    print(f"Error saving product: {e}")
    if mmu_student:
        return redirect(url_for('mmustudent', name=name))
    else:
        return redirect(url_for('notmmustudent', name=name))


@app.route('/')
def homepage():
    name = request.args.get('name')
    products = read_data()
    return render_template('homepage.html', name=name, products=products, mmustudent=mmustudent)

@app.route('/mmustudent/<name>')
def mmustudent(name):  
    products = read_data()
    return render_template("homepage.html",name=name,mmustudent=mmustudent,products=products)


@app.route("/notmmustudent/<name>")
def notmmustudent(name):
    return render_template("homepage.html",name=name)

@app.route("/2-handshop/<name>")
def secondhandshop(name):
    products = read_data()
    return render_template("2-handshop.html",name=name,mmustudent=mmustudent,products=products)

@app.route("/not2-handshop/<name>")
def notsecondhandshop(name):
    products = read_data()
    return render_template("2-handshop.html" ,name=name,products=products)

@app.route("/menspage.html/<name>")
def menspage(name):
    return render_template("menspage.html",name=name,mmustudent=mmustudent)

@app.route("/notmenspage,html/<name>")
def notmenspage(name):
    return render_template("menspage.html",name=name)

@app.route("/womenpage.html/<name>")
def womenpage(name):
    return render_template("womenpage.html",name=name,mmustudent=mmustudent)

@app.route("/notwomenpage.html/<name>")
def notwomenpage(name):
    return render_template("womenpage.html",name=name)

@app.route("/electronicdevice/<name>")
def electronicdevice(name):
    return render_template("electronicdevice.html",name=name,mmustudent=mmustudent)

@app.route("/notelectronicdevice/<name>")
def notelectronicdevice(name):
    return render_template("electronicdevice.html",name=name)

@app.route("/mmustuff/<name>")
def mmustuff(name):
    return render_template("mmustuff.html",name=name,mmustudent=mmustudent)

@app.route("/notmmustuff/<name>")
def notmmustuff(name):
    return render_template("mmustuff.html",name=name)





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
        return render_template("loginpage.html")
    
    
@app.route('/logout')    
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('mmustudent','',expires=0)
    return response





if __name__ == '__main__':
    app.run(debug=True, port=5000)