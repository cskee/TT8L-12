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

def add_to_cart_write_data(add_to_cart_products,name):
    username = name
    print(f'username:{username}')
    try:
        with open('add_to_cart.txt', 'a') as file:
            file.write(f"{add_to_cart_products['username']},{add_to_cart_products['product_name']},{add_to_cart_products['price']},{add_to_cart_products['type']}\n")
            print("Data appended to add_to_cart.txt successfully.")
            print('RM' + add_to_cart_products['price'])

        create_user_file(username)
        user_product_file = f"{username}_products.txt"
        with open(user_product_file, 'a') as file:
            file.write(f"{add_to_cart_products['username']},{add_to_cart_products['product_name']},{add_to_cart_products['price']},{add_to_cart_products['type']}\n")
    except Exception as e:
        print(f"Error writing to add_to_cart.txt: {e}")
        raise

def add_to_cart_read_data(username):
   products = []
   total_price = 0.0
   create_user_file(username)
   user_product_file = f"{username}_products.txt"
   with open(user_product_file, 'r') as file:
       for line in file:
           parts = line.strip().split(',')
           if len(parts) == 4:
               username, product_name, price, p_type = parts
               if 'RM ' in price:
                    try:
                        price = float(price.split('RM ')[1])
                    except (IndexError, ValueError) as e:
                        price = 0.0
                        print(f"Error processing price for {username}: {e}")
               else:
                    price = float(price.strip())
 
               products.append({'username':username,'product_name': product_name, 'price': price, 'type': p_type})
               total_price += price
   return products

def payment_read_data():
    products = []
    with open('add_to_cart.txt','r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4:
                username, product_name, price, p_type = parts
                products.append({'username':username,'product_name': product_name, 'price': price, 'type': p_type})
    return products

def history_read_data():
    products = []
    with open('payment.txt','r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4:
                username, product_name, price, p_type = parts
                products.append({'username':username,'product_name': product_name, 'price': price, 'type': p_type})
    return products



def payment_function(payment_products,name):
    username = name
    with open('payment.txt','a') as file:
        for product in payment_products:
            file.write(f"{product['username']},{product['product_name']},{product['price']},{product['type']}\n")

    updated_lines = []
    with open('add_to_cart.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4 and not any(p['product_name'] == parts[1] for p in payment_products):
                updated_lines.append(line)

    with open('add_to_cart.txt', 'w') as file:
        for line in updated_lines:
            file.write(line)

    deleted_products = []
    create_user_file(username)
    user_product_file = f"{username}_products.txt"
    with open(user_product_file, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4 and not any(p['product_name'] == parts[1] for p in payment_products):
                deleted_products.append(line)

    with open(user_product_file, 'w') as file:
        for line in updated_lines:
            file.write(line)
    



@app.route('/add_to_cart/<name>', methods=['POST'])
def add_to_cart(name):
    if request.method == 'POST':
        username = request.form.get('username')
        name = username
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        product_type = request.form.get('type')

        add_to_cart_products = {
            'username': username,
            'product_name': product_name,
            'price': price,
            'type': product_type,
        }

        
        add_to_cart_write_data(add_to_cart_products,name=name)
        

        if 'RM' in add_to_cart_products['price']:
            return redirect(url_for('mmustudent',name=name)) if name else redirect(url_for('login'))
        else:
            return redirect(url_for('notmmustudent',name=name)) if name else redirect(url_for('login'))
        
    return redirect(url_for('login'))

@app.route('/notadd_to_cart/<name>', methods=['POST'])
def notadd_to_cart(name):
    if request.method == 'POST':
        print(request.form) 
        username = request.form.get('username')
        name = username
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        product_type = request.form.get('type')
        

        if not price.startswith('RM'):
            price = 'RM' + price.strip()

        add_to_cart_products = {
            'username': username,
            'product_name': product_name,
            'price':'RM' + price,
            'type': product_type,
        }
        print(f"Username: {username}, Product Name: {product_name}, Price: {price}, Type: {product_type}")
        try:
            add_to_cart_write_data(add_to_cart_products, name=name)
            flash('Product added successfully', 'success')
            return redirect(url_for('notmmustudent', name=name))
        except Exception as e:
            flash(f'Error adding product: {e}', 'error')
            return redirect(url_for('notmmustudent', name=name))
        
@app.route('/history/<name>')
def history(name):
    payment_products = history_read_data()
    history_products = [product for product in payment_products if product['username'] == name]
    return render_template('history.html',name=name,mmustudent=mmustudent,history_products=history_products)

@app.route('/nothistory/<name>')
def nothistory(name):
    payment_products = history_read_data()
    history_products = [product for product in payment_products if product['username'] == name]
    return render_template('history.html',name=name,history_products=history_products)


@app.route('/some_route/<name>')
def some_route(name):
    print(f'some_route:{name}')
    if mmustudent is True: 
        return redirect(url_for('payment',name=name))
    else:
        return redirect(url_for('notpayment',name=name))

@app.route('/bagtohomepage/<name>')
def bag_to_homepage(name):
    if mmustudent:
        return redirect(url_for('mmustudent',name=name))
    else:
        return redirect(url_for('notmmustudent',name=name))

@app.route('/payment/<name>')
def payment(name):
    payment_products = payment_read_data()
    payment_function(payment_products,name)
    return redirect(url_for('login'))

@app.route('/notpayment/<name>')
def notpayment(name):
    payment_products = payment_read_data()
    payment_function(payment_products,name)
    return redirect(url_for('login'))


@app.route('/add_to_cart/<name>')
def bag(name):
    print(f'name:{name}')
    add_to_cart_products = add_to_cart_read_data(name)
    total_price = sum(item['price'] for item in add_to_cart_products)
    return render_template('cart.html',name=name,add_to_cart_products=add_to_cart_products,total_price=total_price,mmustudent=mmustudent)

@app.route('/notadd_to_cart/<name>')
def notbag(name):
    print(f'name:{name}')
    add_to_cart_products = add_to_cart_read_data(name)
    total_price = sum(item['price'] for item in add_to_cart_products)
    return render_template('cart.html',name=name,add_to_cart_products=add_to_cart_products,total_price=total_price)


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