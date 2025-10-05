Relational Databases & API Rest Development Project | Building an E-commerce API with Flask, SQLAlchemy, Marshmallow, and MySQL
OVERVIEW
In this assignment, you will create a fully functional e-commerce API using Flask, Flask-SQLAlchemy, Flask-Marshmallow, and MySQL. The API will manage Users, Orders, and Products with proper relationships, including One-to-Many and Many-to-Many associations. You will also learn to set up a MySQL database, define models, implement serialization with Marshmallow, and develop RESTful CRUD endpoints.

🎯 LEARNING OBJECTIVES
Database Design: Create models with relationships in SQLAlchemy and MySQL.
API Development: Develop a RESTful API with CRUD operations using Flask.
Serialization: Use Marshmallow schemas for input validation and data serialization.
Testing: Ensure the API is fully functional using Postman and MySQL Workbench
REQUIREMENTS
Set Up MySQL Database
Open MySQL Workbench.
Create a new database named ecommerce_api.
Install Dependencies and Initialize Flask App
Set up a virtual environment:
python3 -m venv venv

Activate the virtual environment:
Mac/Linux: source venv/bin/activate
Windows: venv\Scripts\activate
Install dependencies:
pip install Flask Flask-SQLAlchemy Flask-Marshmallow marshmallow-sqlalchemy mysql-connector-python
DATABASE MODELS
Create the following tables in SQLAlchemy:
User Table
id: Integer, primary key, auto-increment
name: String
address: String
email: String (must be unique)
Order Table
id: Integer, primary key, auto-increment
order_date: DateTime (learn to use DateTime in SQLAlchemy)
user_id: Integer, foreign key referencing User
Product Table
id: Integer, primary key, auto-increment
product_name: String
price: Float
Order_Product Association Table
order_id: Integer, foreign key referencing Order
product_id: Integer, foreign key referencing Product

