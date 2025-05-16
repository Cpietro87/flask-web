import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from models.db import db
from models.products import Products

products = Blueprint('products', __name__, url_prefix='/products')

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@products.route('/')
def get_products():
    products_list = Products.query.all()
    return render_template('products/products.html', products=products_list)


@products.route('/new', methods=['POST'])
def add_product():
    productName = request.form['productName']
    price = request.form['price']
    stock = request.form['stock']
    description = request.form.get('description', '')
    status = bool(request.form.get('status', True))

    image_file = request.files.get('image')
    filename = None

    if image_file and image_file.filename != '':
        if allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)
        else:
            flash('Formato de imagen no permitido. Solo png, jpg, jpeg, gif.', 'danger')
            return redirect(request.referrer)

    new_product = Products(
        productName=productName,
        price=price,
        stock=stock,
        description=description,
        image=filename,
        status=status
    )

    db.session.add(new_product)
    db.session.commit()

    flash('Producto agregado exitosamente!', 'success')
    return redirect(url_for('products.get_products'))


@products.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Products.query.get_or_404(id)

    if request.method == 'POST':
        product.productName = request.form['productName']
        product.price = request.form['price']
        product.stock = request.form['stock']
        product.description = request.form.get('description', '')
        product.status = request.form.get('status') == '1'

        # Manejar imagen
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            if allowed_file(image_file.filename):
                # Borrar imagen vieja
                if product.image:
                    old_image_path = os.path.join(UPLOAD_FOLDER, product.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                # Guardar nueva imagen
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image_file.save(image_path)
                product.image = filename
            else:
                flash(
                    'Formato de imagen no permitido. Solo png, jpg, jpeg, gif.', 'danger')
                return redirect(request.referrer)

        db.session.commit()
        flash('Producto actualizado exitosamente!', 'success')
        return redirect(url_for('products.get_products'))

    return render_template('products/edit_products.html', products=product)


@products.route('/delete/<string:id>', methods=['POST'])
def delete_product(id):
    product = Products.query.get_or_404(id)

    # Borrar imagen si existe
    if product.image:
        image_path = os.path.join(UPLOAD_FOLDER, product.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado exitosamente!', 'success')
    return redirect(url_for('products.get_products'))
