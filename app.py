from flask import Flask, render_template, request, redirect, jsonify
from models import db, Merchant, Product, Price
from config import Config
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# إنشاء الجداول في قاعدة البيانات
with app.app_context():
    db.create_all()

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# إضافة تاجر
@app.route('/add_merchant', methods=['GET', 'POST'])
def add_merchant():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        new_merchant = Merchant(name=name, phone=phone, email=email)
        db.session.add(new_merchant)
        db.session.commit()
        return redirect('/')
    return render_template('add_merchant.html')

# تعديل صفحة إضافة القطع لعرض القطع والفئات المسجلة مسبقًا
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    merchants = Merchant.query.all()  # جلب التجار
    products = Product.query.all()    # جلب أسماء القطع
    categories = db.session.query(Product.category).distinct()  # جلب الفئات المميزة
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        merchant_id = request.form['merchant_id']
        wholesale_price = request.form['wholesale_price']
        retail_price = request.form['retail_price']
        
        # إذا كانت القطعة جديدة، أضفها إلى قاعدة البيانات
        new_product = Product(name=name, category=category, description=description)
        db.session.add(new_product)
        db.session.commit()

        # أضف السعر الجديد
        new_price = Price(merchant_id=merchant_id, product_id=new_product.id, wholesale_price=wholesale_price, retail_price=retail_price)
        db.session.add(new_price)
        db.session.commit()
        
        return redirect('/')
    return render_template('add_product.html', merchants=merchants, products=products, categories=categories)

# عرض قطع الغيار
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

# إضافة صفحة للبحث مع فلاتر
@app.route('/search', methods=['GET', 'POST'])
def search():
    products = []
    merchants = Merchant.query.all()
    categories = db.session.query(Product.category).distinct()
    
    if request.method == 'POST':
        name_filter = request.form.get('name_filter')
        category_filter = request.form.get('category_filter')
        merchant_filter = request.form.get('merchant_filter')
        
        query = Product.query
        
        # تطبيق الفلاتر
        if name_filter:
            query = query.filter(Product.name.like(f"%{name_filter}%"))
        if category_filter:
            query = query.filter(Product.category.like(f"%{category_filter}%"))
        if merchant_filter:
            query = query.join(Price).filter(Price.merchant_id == merchant_filter)
        
        products = query.all()
    
    return render_template('search.html', products=products, merchants=merchants, categories=categories)

# إضافة مسار لحذف تاجر
@app.route('/delete_merchant/<int:merchant_id>', methods=['POST'])
def delete_merchant(merchant_id):
    merchant = Merchant.query.get_or_404(merchant_id)
    db.session.delete(merchant)
    db.session.commit()
    return redirect('/merchants')  # إعادة التوجيه إلى صفحة التجار

# إضافة مسار لحذف قطعة غيار
@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/products')  # إعادة التوجيه إلى صفحة عرض المنتجات

if __name__ == '__main__':
    app.run(debug=True)
