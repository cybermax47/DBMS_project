from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password1@localhost/travelers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model definitions
class Package(db.Model):
    __tablename__ = 'packages'
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

# Route to serve the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to get all packages
@app.route('/api/packages', methods=['GET'])
def get_packages():
    packages = Package.query.all()
    return jsonify([package.to_dict() for package in packages])

# Route to get a single package by ID
@app.route('/api/packages/<int:package_id>', methods=['GET'])
def get_package(package_id):
    package = Package.query.get_or_404(package_id)
    return jsonify(package.to_dict())

# Route to add a new package
@app.route('/api/packages', methods=['POST'])
def add_package():
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
@app.route('/api/packages/<int:package_id>', methods=['PUT'])
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
@app.route('/api/packages/<int:package_id>', methods=['DELETE'])
def delete_package(package_id):
    package = Package.query.get_or_404(package_id)
    db.session.delete(package)
    db.session.commit()
    return jsonify({'message': 'Package deleted'})

if __name__ == '__main__':
    app.run(debug=True)

def fetch_discounted_packages(price_threshold):
    """
    Fetches packages that have a discount price below the specified threshold.

    Args:
    price_threshold (float): The maximum price to qualify as discounted.

    Returns:
    list of dict: A list of dictionaries, each representing a discounted package.
    """
    try:
        # Ensure connection is available
        conn = db.engine.connect()
        query = """
        SELECT package_id, destination, description, price, discount_price, image_url
        FROM packages
        WHERE discount_price IS NOT NULL AND discount_price <= :price_threshold;
        """
        # Execute the query with a safe parameter substitution
        result = conn.execute(query, {'price_threshold': price_threshold})
        # Fetch all results
        packages = result.fetchall()
        # Close the connection
        conn.close()
        
        # Convert the results into a list of dictionaries
        package_list = [
            {
                'package_id': row[0],
                'destination': row[1],
                'description': row[2],
                'price': float(row[3]),
                'discount_price': float(row[4]),
                'image_url': row[5]
            } for row in packages
        ]
        return package_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
