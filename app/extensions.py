from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# db is our database helper.
# migrate manages database schema changes.

db = SQLAlchemy()
migrate = Migrate()
