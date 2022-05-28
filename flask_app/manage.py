# from flask_migrate import Migrate
# from flask_script import Manager
from app import app

# manager = Manager(app)

# Database migrations command
# manager.add_command('db', Migrate)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
