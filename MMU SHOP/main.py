from flask import Flask, redirect, url_for, render_template, request, make_response, flash
import os

app = Flask(__name__)
app.secret_key = 'yoo'

mmu_student = False

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_user_file(username):
    user_product_file = f"{username}_products.txt"
    with open(user_product_file, 'a') as file:
        pass  

def write_data(product, username):
    with open('all_the_products.txt','a') as file:
        file.write(f"{product['username']},{product['product_name']},{product['price']},{product['type']},{product['image']}\n")

    
    create_user_file(username)
    user_product_file = f"{username}_products.txt"
    with open(user_product_file, 'a') as file:
        file.write(f"{product['username']},{product['product_name']},{product['price']},{product['type']},{product['image']}\n")

    

def delete_data(product, username):
    updated_lines = []
    with open('all_the_products.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if parts[0] == product['product_name']:
                print(f"Deleted product: {line.strip()}")  
                continue
            updated_lines.append(line)
    with open('all_the_products.txt', 'w') as file:
        for line in updated_lines:
            file.write(line)

    updated_lines = []
    user_product_file = f"{username}_products.txt"
    with open(user_product_file, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if parts[0] == product['product_name']:
                print(f"Deleted product: {line.strip()}")  
                continue
            updated_lines.append(line)
    with open(user_product_file, 'w') as file:
        for line in updated_lines:
            file.write(line)


def read_data(username):
    products = []
    with open("all_the_products.txt", 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 5:
                username, product_name, price, p_type, image = parts
                products.append({'username':username,'product_name': product_name, 'price': price, 'type': p_type, 'image': image})
    return products

@app.route('/uploadproduct/<name>')
def uploadproduct(name):
    return render_template("sellerform.html", name=name,mmustudent=mmustudent)

@app.route('/notuploadproduct/<name>')
def notuploadproduct(name):
    return render_template("sellerform.html", name=name)
  
@app.route("/product", methods=['POST', 'GET'])
def product():
    name = request.form.get('username')
    print(f"name:{name}")
    username = name
    if 'delete' in request.form:
        product_name_to_delete = request.form['delete']
        try:
            delete_data({'product_name': product_name_to_delete},  username = name)
            flash('Product deleted successfully', 'success')  
        except Exception as e:
            flash(f'Error deleting product: {e}', 'error')  
        return redirect(url_for('mmustudent', name= username))
    else:
        if request.method == 'POST':
            if 'image' not in request.files:
                flash('No image file selected', 'error')
                return redirect(request.url)
            file = request.files['image']
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                try:
                    username=username
                    filename = file.filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    new_product = {
                        'username': request.form['username'],
                        'product_name': request.form['product_name'],
                        'price': request.form['price'],
                        'type': request.form['type'],
                        'image': filename
                    }
                    write_data(new_product, username)

                    if new_product['type'] == '2-handshop':
                        flash('Product added successfully', 'success')
                        return redirect(url_for('secondhandshop', username=username))
                    if new_product['type'] == 'men':
                        flash('Product added successfully', 'success')
                        return redirect(url_for('menspage', username=username))

                except Exception as e:
                    flash(f'Error saving product: {e}', 'error')
    return redirect(url_for('mmustudent', name=name)) if name else redirect(url_for('login'))  

@app.route('/')
def homepage():
    name = request.args.get('name')
    products = read_data(name) if name else []
    return render_template('homepage.html', name=name, products=products, mmustudent=mmustudent)


@app.route('/mmustudent/<name>')
def mmustudent(name):
    username = name
    all_products = read_data(username)
    secondhand_products = [product for product in all_products if product['type'] == '2-handshop']
    mens_products = [product for product in all_products if product['type'] == 'men']
    womens_products = [product for product in all_products if product['type'] == 'women']
    electronic_device_products = [product for product in all_products if product['type'] == 'electronic-device']
    mmu_stuff_products = [product for product in all_products if product['type'] == 'mmu_stuff']
    return render_template("homepage.html", name=name, mmustudent=mmustudent, products=all_products,secondhand_products=secondhand_products,mens_products=mens_products,womens_products=womens_products,electronic_device_products=electronic_device_products,mmu_stuff_products=mmu_stuff_products)


@app.route('/notmmustudent/<name>')
def notmmustudent(name):
    username = name
    all_products = read_data(username)
    secondhand_products = [product for product in all_products if product['type'] == '2-handshop']
    mens_products = [product for product in all_products if product['type'] == 'men']
    womens_products = [product for product in all_products if product['type'] == 'women']
    electronic_device_products = [product for product in all_products if product['type'] == 'electronic-device']
    mmu_stuff_products = [product for product in all_products if product['type'] == 'mmu_stuff']
    return render_template("homepage.html", name=name, products=all_products,secondhand_products=secondhand_products,mens_products=mens_products,womens_products=womens_products,electronic_device_products=electronic_device_products,mmu_stuff_products=mmu_stuff_products)


@app.route('/2-handshop/<name>')
def secondhandshop(name):
    username = name
    all_products = read_data(username)
    products = [product for product in all_products if product['type'] == '2-handshop']
    return render_template('2-handshop.html',name=name,mmustudent=mmustudent,products=products)

@app.route("/not2-handshop/<name>")
def notsecondhandshop(name):
    username = name
    all_products = read_data(username)
    products = [product for product in all_products if product['type'] == '2-handshop']
    return render_template("2-handshop.html" ,name=name,products=products)

@app.route("/menspage.html/<name>")
def menspage(name):
    username = name
    all_products = read_data(username)
    products = [product for product in all_products if product['type'] == 'men']
    return render_template("menspage.html",name=name,mmustudent=mmustudent,products=products)

@app.route("/notmenspage,html/<name>")
def notmenspage(name):
    username = name
    all_products = read_data(username)
    products = [product for product in all_products if product['type'] == 'men']
    return render_template("menspage.html",name=name,products=products)

@app.route("/womenpage.html/<name>")
def womenpage(name):
    username = name
    all_products = read_data(username)
    products = [product for product in all_products if product['type'] == 'women']
    return render_template("womenpage.html",name=name,mmustudent=mmustudent,products=products)

@app.route("/notwomenpage.html/<name>")
def notwomenpage(name):
    username = name
    all_products = read_data(username)
    products = [product for product in all_products if product['type'] == 'women']
    return render_template("womenpage.html",name=name,products=products)

@app.route("/electronicdevice/<name>")
def electronicdevice(name):
    username = name
    all_products = read_data(username)
    products = [product for product in all_products if product['type'] == 'electronic-device']
    return render_template("electronicdevice.html",name=name,mmustudent=mmustudent,products=products)

@app.route("/notelectronicdevice/<name>")
def notelectronicdevice(name):
    username = name
    all_products = read_data(username)
    products = [product for product in all_products if product['type'] == 'electronic-device']
    return render_template("electronicdevice.html",name=name,products = products)

@app.route("/mmustuff/<name>")
def mmustuff(name):
    username = name
    all_products = read_data(username)
    products = [product for product in all_products if product['type'] == 'mmu_stuff']
    return render_template("mmustuff.html",name=name,mmustudent=mmustudent,products=products)

@app.route("/notmmustuff/<name>")
def notmmustuff(name):
    username = name
    all_products = read_data(username)
    products = [product for product in all_products if product['type'] == 'mmu_stuff']
    return render_template("mmustuff.html",name=name,products=products)


@app.route('/login', methods=['POST', 'GET'])
def login():
    global mmu_student
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if "@student.mmu.edu.my" in email:
            mmu_student = True
            username = email.split('@')[0]
            create_user_file(username)
            return redirect(url_for('mmustudent', name=username))
        else:
            mmu_student = False
            username = email.split('@')[0]
            return redirect(url_for('notmmustudent', name=username))
    else:
        return render_template("loginpage.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)