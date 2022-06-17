# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# init app
app = Flask(__name__)


#Databade
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
app.config['SQLALCHEMY_BINDS'] = {'car':'sqlite:///car.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize db
db = SQLAlchemy(app)


# init marshmallow
ma = Marshmallow(app)


class Car(db.Model):
    __bind_key__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    company = db.Column(db.String(200), unique=True)

    def __init__(self, name, price, company):
        self.name = name
        self.price = price
        self.company = company

#creating the car schema

class CarSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'company')


# init Schema
car_schema = CarSchema()
cars_schema = CarSchema(many=True)


@app.route('/', methods=['GET'])
def get():
    return jsonify({"msg": "i am working"})

@app.route('/car', methods=['POST'])
def add_car():
    data = request.get_json()
    name = data['name']
    price = data['price']
    company = data['company']

    new_car = Car(name, price, company)
    db.session.add(new_car)
    db.session.commit()

    return car_schema.jsonify(new_car)






# Get all car
@app.route('/car', methods=['GET'])
def get_cars():
    all_cars = Car.query.all()
    result = cars_schema.dump(all_cars)
    return jsonify(result)




# Get single products
@app.route('/car/<id>', methods=['GET'])
def get_car(id):
    car = Car.query.get(id)
    return car_schema.jsonify(car)




# update Car
@app.route('/car/<id>', methods=['PUT'])
def update_car(id):
    car = Car.query.get(id)

    data = request.get_json()
    name = data['name']

    price = data['price']
    company = data['company']

    car.name = name
    car.price = price
    car.company = company

    db.session.commit()

    return blog_schema.jsonify(car)



# Delete single car
@app.route('/car/<id>', methods=['DELETE'])
def delete_car(id):
    car = Car.query.get(id)

    db.session.delete(car)
    db.session.commit()
    return car_schema.jsonify(car)




# Blog class/model
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_name = db.Column(db.String(300))
    author = db.Column(db.String(200))
    subject = db.Column(db.String(200))
    body = db.Column(db.String(5000))

    def __init__(self, blog_name, author, subject, body):
        self.blog_name = blog_name
        self.author = author
        self.subject = subject
        self.body = body

#Blog Schema
class BlogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'blog_name', 'author', 'subject', 'body')

# init Schema

blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)



@app.route('/' ,  methods=['GET'])
def hello():
    return jsonify({'msg': 'Hi'})

# create a blog
@app.route('/blog', methods=['POST'])
def add_blog():
    data = request.get_json()
    blog_name = data['blog_name']

    author = data['author']
    subject = data['subject']
    body = data['body']

    new_blog = Blog(blog_name, author, subject, body)

    db.session.add(new_blog)
    db.session.commit()

    return blog_schema.jsonify(new_blog)

# Get all Blogs
@app.route('/blog', methods=['GET'])
def get_blogs():
    all_blogs = Blog.query.all()
    result = blogs_schema.dump(all_blogs)
    return jsonify(result)


# Get single products
@app.route('/blog/<id>', methods=['GET'])
def get_blog(id):
    blog = Blog.query.get(id)
    return blog_schema.jsonify(blog)





# update Blog
@app.route('/blog/<id>', methods=['PUT'])
def update_blog(id):
    blog = Blog.query.get(id)

    data = request.get_json()
    blog_name = data['blog_name']

    author = data['author']
    subject = data['subject']
    body = data['body']

    blog.blog_name = blog_name
    blog.author = author
    blog.subject = subject
    blog.body = body


    db.session.commit()

    return blog_schema.jsonify(blog)



# Delete single products
@app.route('/blog/<id>', methods=['DELETE'])
def delete_blog(id):
    blog = Blog.query.get(id)

    db.session.delete(blog)
    db.session.commit()
    return blog_schema.jsonify(blog)

db.create_all()



if __name__ == '__main__':
    app.run(debug=True)
