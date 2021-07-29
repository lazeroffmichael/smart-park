from flask import Flask
from flask_restful import Api

# Blueprint handling
from api.initialize_routes import initialize_routes

# Main flask application global variables
app = Flask(__name__)
api = Api(app)

# Initialize the routes
initialize_routes(api)

if __name__ == '__main__':
    app.run(debug=True)
