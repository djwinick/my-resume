from flask_script import Manager
from resume import app, db, Professor, Course

manager = Manager(app)


# reset the database and create two artists
@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    monk = Professor(name='Ellen Monk', dept='MIS')
    bayley = Professor(name='Elizabeth Bayley', dept='ECON')
    MISY261 = Course(number='MISY261', title='Business Information Systems', desc='Introduction to management information systems', professor=monk)
    MISY380 = Course(number='MISY380', title='Enterprise Resource Planning Systems', desc='Focuses on large scale enterprise resource planning systems, their development, functionality, and implementation', professor=monk)
    ECON101 = Course(number='ECON101', title='Introduction to Microeconomics', desc='Introduces supply and demand concepts with basic economic graphs', professor=bayley)
    ECON300 = Course(number='ECON300', title='Intermediate Microeconomic Theory', desc='Price determination and income distribution in a market economy; the behavior of firms and industry under conditions of pure and imperfect competition', professor=bayley)
    db.session.add(monk)
    db.session.add(bayley)
    db.session.add(MISY261)
    db.session.add(MISY380)
    db.session.add(ECON101)
    db.session.add(ECON300)
    db.session.commit()


@manager.command
def hello():
    print "hello"


if __name__ == "__main__":
    manager.run()
