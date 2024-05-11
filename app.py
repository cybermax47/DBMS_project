#THIS IS THE APP.PY
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:database1@localhost/travelers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: to suppress a warning from SQLAlchemy
db = SQLAlchemy(app)

# Define a model for the packages
class Package(db.Model):
    package_id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    discount_price = db.Column(db.Numeric(6, 2))
    image_url = db.Column(db.String(255))

    def to_dict(self):
        return {
            'package_id': self.package_id,
            'destination': self.destination,
            'description': self.description,
            'price': float(self.price),
            'discount_price': float(self.discount_price) if self.discount_price else None,
            'image_url': self.image_url
        }

# Route to get all packages
@app.route('/packages', methods=['GET'])
def get_packages():
    packages = Package.query.all()
    return jsonify([package.to_dict() for package in packages])

# Route to get a single package by ID
@app.route('/packages/<int:package_id>', methods=['GET'])
def get_package(package_id):
    package = Package.query.get_or_404(package_id)
    return jsonify(package.to_dict())

# Route to create a new package
@app.route('/packages', methods=['POST'])
def create_package():
    data = request.get_json()
    new_package = Package(
        destination=data['destination'],
        description=data['description'],
        price=data['price'],
        discount_price=data.get('discount_price'),
        image_url=data.get('image_url')
    )
    db.session.add(new_package)
    db.session.commit()
    return jsonify(new_package.to_dict()), 201

# Route to update a package
@app.route('/packages/<int:package_id>', methods=['PUT'])
def update_package(package_id):
    package = Package.query.get_or_404(package_id)
    data = request.get_json()
    package.destination = data.get('destination', package.destination)
    package.description = data.get('description', package.description)
    package.price = data.get('price', package.price)
    package.discount_price = data.get('discount_price', package.discount_price)
    package.image_url = data.get('image_url', package.image_url)
    db.session.commit()
    return jsonify(package.to_dict())

# Route to delete a package
@app.route('/packages/<int:package_id>', methods=['DELETE'])
def delete_package(package_id):
    package = Package.query.get_or_404(package_id)
    db.session.delete(package)
    db.session.commit()
    return jsonify({'message': 'Package deleted'})
#this is a main function
# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
