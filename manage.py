from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db
from app.model.user_model import User
from app.model.single_choice_model import SingleChoice
from app.model.blank_fill_model import BlankFill
from app.model.essay_model import Essay
from app.model.point_model import Points
from app.model.subject_model import Subject

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, SingleChoice=SingleChoice,
                BlankFill=BlankFill, Essay=Essay, Points=Points,
                Subject=Subject)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
