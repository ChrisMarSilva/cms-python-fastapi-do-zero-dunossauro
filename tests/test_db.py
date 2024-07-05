from sqlalchemy import select

from app.models.user import User


def test_db_users_create(session):
    # Arrange
    new_user = User(username='chrismarsil', password='123@456', email='chrismarsil@server.com')

    # Act
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Assert
    assert new_user.id == 1
    assert new_user.username == 'chrismarsil'
    assert new_user.password == '123@456'
    assert new_user.email == 'chrismarsil@server.com'
    expected_repr = f'User(id={new_user.id!r}, username={new_user.username!r}, password={new_user.password!r}, email={new_user.email!r}, created_at={new_user.created_at.strftime("%d-%m-%Y %H:%M:%S")!r}, updated_at={new_user.updated_at.strftime("%d-%m-%Y %H:%M:%S")!r})'
    assert repr(new_user) == expected_repr
    # assert f'id={user.id!r},' in repr(user)
    # assert f'username={user.username!r},' in repr(user)
    # assert f'password={user.password!r},' in repr(user)
    # assert f'email={user.email!r},' in repr(user)
    # assert f'created_at={user.created_at.strftime("%d-%m-%Y %H:%M:%S")!r},' in repr(user)
    # assert f'updated_at={user.updated_at.strftime("%d-%m-%Y %H:%M:%S")!r},' in repr(user)


def test_db_users_create_and_read(session, user):
    # Arrange
    new_user = User(username='chrismarsil', password='123@456', email='chrismarsil@server.com')
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Act
    stmt = select(User).where(User.username == new_user.username)
    bd_user = session.scalar(stmt)

    # Assert
    assert bd_user.id == new_user.id
    assert bd_user.username == new_user.username
    assert bd_user.password == new_user.password
    assert bd_user.email == new_user.email
