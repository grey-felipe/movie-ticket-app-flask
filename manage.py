import os
import unittest
import coverage
import config

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.api.accounts.models import User, TokenBlacklist

from app.api import create_app, db
from app import v1_blueprint


app = create_app(os.environ["BOILERPLATE_ENV"] or "dev")
app.register_blueprint(v1_blueprint, url_prefix="/api/v1")
app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

# Test coverage command
# pytest --cov --cov-report html tests/


if __name__ == '__main__':
    manager.run()
