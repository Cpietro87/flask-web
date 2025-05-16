from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db
from routes.products_routes import products
from routes.about import about

app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.register_blueprint(products)
app.register_blueprint(about)


app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    from models.products import Products
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
