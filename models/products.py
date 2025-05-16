import uuid
from models.db import db

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    productName = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Boolean, default=True)

    def __init__(self, productName, price, stock, description=None, image=None, status=True):
        self.productName = productName
        self.price = price
        self.stock = stock
        self.description = description
        self.image = image
        self.status = status

    def serialize(self):
        return {
            'id': self.id,
            'productName': self.productName,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'image': self.image,
            'status': self.status
        }

   