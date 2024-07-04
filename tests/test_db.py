from sqlalchemy import select

from app.models.user import User


def test_db_users_create(session):
    # Arrange
    user = User(username='chrismarsil', password='123@456', email='chrismarsil@server.com')

    # Act
    session.add(user)
    session.commit()
    session.refresh(user)

    # Assert
    assert user.id == 1
    assert user.username == 'chrismarsil'
    assert user.password == '123@456'
    assert user.email == 'chrismarsil@server.com'


def test_db_users_create_and_read(session):
    # Arrange
    new_user = User(username='chrismarsil', password='123@456', email='chrismarsil@server.com')
    session.add(new_user)
    session.commit()

    # Act
    stmt = select(User).where(User.username == 'chrismarsil')
    user = session.scalar(stmt)

    # Assert
    assert user.id == 1
    assert user.username == 'chrismarsil'
    assert user.password == '123@456'
    assert user.email == 'chrismarsil@server.com'
