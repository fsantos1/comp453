from flask import Flask, render_template,request,json,redirect,session
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'fabricioricci'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Italia10!!'
app.config['MYSQL_DATABASE_DB'] = 'gpackers'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
Bootstrap(app)


@app.route("/")
def main():
    return render_template('index4.html')
    
@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')
    
@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')
	
@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')
		
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')
	
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
		
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()
        

@app.route("/product/new", methods=['GET', 'POST'])
@login_required
def new_product():
    form = DeptForm()
    if form.validate_on_submit():
        dept = Department(ProductID=form.ProductID.data, NameOfProduct=form.NameOfProduct.data,Manufacturer=form.Manufacturer.data,Price=form.Price.data, RAM=form.RAM.data, ScreenSize=form.ScreenSize.data)
        db.session.add(dept)
        db.session.commit()
        flash('You have added a new product!', 'success')
        return redirect(url_for('home'))
    return render_template('createproducts.html', title='New Product',
                           form=form, legend='New Product')
						   
						   
@app.route("/prod/<ProductID>")
@login_required
def prod(ProductID):
    prod = products.query.get_or_404(dnumber)
    return render_template('prod.html', title=prod.NameOfProduct, prod=prod, now=datetime.utcnow())						   
						   
@app.route("/prod/<ProductID>/update", methods=['GET', 'POST'])
@login_required
def update_product(ProductID):
    prod = products.query.get_or_404(ProductID)
    currentProd = prod.NameOfProduct

    form = ProdUpdateForm()
    if form.validate_on_submit():          
        if currentProd !=form.NameOfProduct.data:
            dept.NameOfProduct=form.NameOfProduct.data
        dept.mgr_ssn=form.mgr_ssn.data
        dept.mgr_start=form.mgr_start.data
        db.session.commit()
        flash('Your product has been updated!', 'success')
        return redirect(url_for('prod', ProductID=ProductID))
    elif request.method == 'GET':              

        form.ProductID.data = prod.ProductID
        form.NameOfProduct.data = prod.NameOfProduct
        form.Manufacturer.data = prod.Manufacturer
        form.Price.data = prod.Price
		form.RAM.data = prod.RAM
        form.ScreenSize.data = prod.ScreenSize
    return render_template('createproducts.html', title='Update Product',
                           form=form, legend='Update Department')



@app.route("/dept/<ProductID>/delete", methods=['POST'])
@login_required
def delete_product(ProductID):
    prod = products.query.get_or_404(ProductID)
    db.session.delete(prod)
    db.session.commit()
    flash('The product has been deleted!', 'success')
    return redirect(url_for('home'))
	

@app.route('/manufacturers')
def manufacturers():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT Manufacturer FROM products")
    if resultValue > 0:
        prodDetails = cur.fetchall()
        return render_template('manufacturers.html',data=prodDetails)
		
@app.route('/totalsum')
def totalsum():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT SUM(Price) FROM products")
    if resultValue > 0:
        prodDetails = cur.fetchall()
        return render_template('manufacturers.html',data=prodDetails)
		
@app.route('/ramrange')
def ramrange():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM products WHERE RAM > 90 AND RAM <= 150")
    if resultValue > 0:
        prodDetails = cur.fetchall()
        return render_template('manufacturers.html',data=prodDetails)
		
@app.route('/totalcostofproduct')
def totalcostofproduct():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM products WHERE RAM > 90 AND RAM <= 150")
    if resultValue > 0:
        prodDetails = cur.fetchall()
        return render_template('manufacturers.html',data=prodDetails)
		
@app.route('/expensiveproducts')
def expensiveproducts():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT ProductID FROM products WHERE Price > (SELECT AVG(Price) FROM products)")
    if resultValue > 0:
        prodDetails = cur.fetchall()
        return render_template('manufacturers.html',data=prodDetails)
		
@app.route('/totalquantity')
def totalquantity():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT ProductID, (SELECT SUM(Quantity) FROM orderdetails WHERE ProductID=products.ProductID) AS 'total sold' FROM products")
    if resultValue > 0:
        prodDetails = cur.fetchall()
        return render_template('manufacturers.html',data=prodDetails)

@app.route('/joinquery')
def joinquery():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT od.OrderNumber, od.ProductID, p.NameOfProduct, od.Price, od.Quantity, (od.Price * od.Quantity) AS 'total cost' FROM orderdetails AS od INNER JOIN products AS p ON p.ProductID = od.ProductID")
    if resultValue > 0:
        prodDetails = cur.fetchall()
        return render_template('manufacturers.html',data=prodDetails)		
	
	
if __name__ == '__main__':
    app.run(port=5002)			