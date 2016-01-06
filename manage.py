from app import create_app, config
from app.utils import parse_sqlalchemy_url,invoke_process
from app.database import db, populate_db
#from flask.ext.migrate import Migrate, MigrateCommand
from flask_migrate import MigrateCommand as db_manager
from flask_migrate import Migrate
import os
from flask.ext.script import (
    Server,
    Shell,
    Manager,
    prompt_bool,
)


def _make_context():
    return dict(
        app=create_app(config.dev_config),
        db=db,
        populate_db=populate_db
    )

app = create_app(config=config.dev_config)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=_make_context))
#manager.add_command('db', MigrateCommand)
manager.add_command('db', db_manager)

@db_manager.option('--url', dest='url', type=parse_sqlalchemy_url,
                   default=app.config['SQLALCHEMY_DATABASE_URI'],
                   help="A RFC1738 URL to a PostgreSQL or SQLite database to use.")
def repl(url):
    """
    Usage: ./manage.py db repl
    Launch a psql or sqlite3 repl connected to the database
    """
    def build_named_arglist(arg_dict):
        for name, value in arg_dict.iteritems():
            yield "--{}".format(name)
            yield str(value)

    dialect = url.get_dialect()
    if dialect.name == "postgresql":
        env = os.environ.copy()
        env["PGPASSWORD"] = url.password
        proc_args = list(build_named_arglist({
            'host': url.host,
            'port': url.port,
            'username': url.username,
            'dbname': url.database
        }))
        return invoke_process("psql", proc_args, env=env)
    elif dialect.name == "sqlite":
        proc_args = [url.database] if url.database else []
        return invoke_process("sqlite3", proc_args)
    else:
        raise argparse.ArgumentTypeError("Dialect {} is not supported.".format(dialect.name))

@manager.command
@manager.option('-n', '--num_users', help='Number of users')
def create_db(num_users=5):
    """Creates database tables and populates them."""
    db.create_all()
    populate_db(num_users=num_users)


@manager.command
def drop_db():
    """Drops database tables."""
    if prompt_bool('Are you sure?'):
        db.drop_all()


@manager.command
def recreate_db():
    """Same as running drop_db() and create_db()."""
    drop_db()
    create_db()


if __name__ == '__main__':
    manager.run()
