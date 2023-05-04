from flask.cli import FlaskGroup
from app import app, db

cli = FlaskGroup(app)

@cli.command('create_db')
def create_db():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    cli()