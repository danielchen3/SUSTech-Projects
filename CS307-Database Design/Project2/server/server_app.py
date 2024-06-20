# app/server/app.py
from config import Config
from flask import Flask
# from peewee import PostgresqlDatabase
from routes import create_routes

app = Flask(__name__)
app.config.from_object(Config)

if __name__ == '__main__':
    app = create_routes(app)
    app.run(debug=True)
