from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey, Table, DateTime
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Yeshua2025%40%23@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating our Base Model
class Base(DeclarativeBase):
    pass
#Initialize extensions
# Register the Flask app with the SQLAlchemy instance so the extension
# knows about the current app (prevents RuntimeError about app not being
# registered). Alternatively you could call `db.init_app(app)` after
# creating `db` if you prefer the factory pattern.
db = SQLAlchemy(app, model_class=Base)
ma = Marshmallow(app)

# Association Table
order_product = db.Table(
    "order_product",
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True)
)
# User model
class User(db.Model):
    
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    orders = db.relationship("Order", back_populates="user", cascade="all, delete")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="orders")
    products = db.relationship("Product", secondary=order_product, back_populates="orders")

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    orders = db.relationship("Order", secondary=order_product, back_populates="products")

# Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True
        load_instance = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True
        load_instance = True
    user = ma.Nested(UserSchema)
    products = ma.Nested(ProductSchema, many=True)

# CRUD for Users
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    new_user = User(name=data["name"], address=data["address"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return user_schema.jsonify(user)

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.name = data.get("name", user.name)
    user.address = data.get("address", user.address)
    user.email = data.get("email", user.email)
    db.session.commit()
    return user_schema.jsonify(user)

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

# Initialize
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)