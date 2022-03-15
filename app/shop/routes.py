from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required


shop = Blueprint('shop', __name__, template_folder='shop_templates')

from app.models import db, Product, Cart
from .forms import CreateProductForm

@shop.route('/products')
def allProducts():
    products = Product.query.all()
    return render_template('shop.html', products)

@shop.route('/posts/<int:product_id>')
def individualProduct(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if product is None:
        return redirect(url_for('shop.allProducts'))
    return render_template('individual_product.html', product = product)

@shop.route('/products/create')
@login_required
def createProduct():
    if current_user.is_admin:
        form = CreateProductForm()
        if request.method == "POST":
            if form.validate():
                product_name = form.product_name.data
                img_url = form.img_url.data
                description = form.description.data
                price = form.price.data

                product = Product(product_name, img_url, description, price)

                db.session.add(product)
                db.session.commit()   

                return redirect(url_for('shop.createProduct'))
    else:
        return redirect(url_for('shop.allProducts'))

    return render_template('create_product.html', form = form)