from app.models.user import User
from app.repositories.user import UserRepository


def test_db_users_create(session):
    # Arrange
    new_user = User(username='chrismarsil', password='123@456', email='chrismarsil@server.com')

    # Act
    new_user = UserRepository.create(session=session, user=new_user)

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


def test_db_users_read_all(session, user):
    bd_user = UserRepository.get_all(session=session, skip=0, limit=100)
    assert bd_user[0].id == user.id


def test_db_users_read_one_by_id(session, user):
    bd_user = UserRepository.get_by_id(session=session, user_id=user.id)
    assert bd_user.id == user.id


def test_db_users_read_one_by_username(session, user):
    bd_user = UserRepository.get_by_username(session=session, username=user.username)
    assert bd_user.id == user.id


def test_db_users_read_one_by_email(session, user):
    bd_user = UserRepository.get_by_email(session=session, email=user.email)
    assert bd_user.id == user.id


def test_db_users_read_one_by_username_or_email(session, user):
    bd_user = UserRepository.get_by_username_or_email(session=session, username=user.username, email=user.email)
    assert bd_user.id == user.id


def test_db_users_exists_by_id(session, user):
    result = UserRepository.exists_by_id(session=session, user_id=user.id)
    assert result is True


def test_db_users_update(session, user):
    user.username = 'chrismarsil2'
    bd_user = UserRepository.update(session=session, user=user)
    assert bd_user.username == 'chrismarsil2'


def test_db_users_delete(session, user):
    UserRepository.delete(session=session, user=user)
    result = UserRepository.exists_by_id(session=session, user_id=user.id)
    assert result is False
