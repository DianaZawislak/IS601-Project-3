from sqlalchemy.testing import db

from app.db.models import User


def test_register(client):
    """ POST to /register """
    new_email = 'newuser@test.test'
    new_password = 'Test1234!'
    data = {
        'email' : new_email,
        'password' : new_password,
        'confirm' : new_password
    }
    resp = client.post('register', data=data)

    assert resp.status_code == 302

    # verify new user is in database
    new_user = User.query.filter_by(email=new_email).first()
    assert new_user.email == new_email

    db.session.delete(new_user) # pylint: disable=no-member


def test_login(client, add_db_user_fixture):
    """ POST to login """
    data = {
        'email' : 'testuser@test.com',
        'password' : 'testtest'
    }
    resp = client.post('login', data=data)

    assert resp.status_code == 302