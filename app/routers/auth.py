from http import HTTPStatus
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.models.user import User
from app.schemas.token import TokenRequest
from app.utils.security import create_access_token, verify_password

router = APIRouter()
OAuth2FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
SessionDep = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=TokenRequest, status_code=HTTPStatus.OK)
async def login_for_access_token(form_data: OAuth2FormDep, session: SessionDep) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    stmt = select(User).where(User.email == form_data.username)
    user = session.scalar(stmt)

    if not user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Incorrect email or password')

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Incorrect email or password')

    access_token = create_access_token(data={'sub': user.email, 'id': user.id, 'username': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


# @router.post("/test-token", response_model=UserPublic)
# def test_token(current_user: CurrentUser) -> Any:
#     """
#     Test access token
#     """
#     return current_user
#
#
# @router.post("/password-recovery/{email}")
# def recover_password(email: str, session: SessionDep) -> Message:
#     """
#     Password Recovery
#     """
#     user = crud.get_user_by_email(session=session, email=email)
#     if not user:
#         raise HTTPException(status_code=404, detail="The user with this email does not exist in the system.")
#     password_reset_token = generate_password_reset_token(email=email)
#     email_data = generate_reset_password_email(email_to=user.email, email=email, token=password_reset_token)
#     send_email(email_to=user.email, subject=email_data.subject, html_content=email_data.html_content)
#     return Message(message="Password recovery email sent")
#
#
# @router.post("/reset-password/")
# def reset_password(session: SessionDep, body: NewPassword) -> Message:
#     """
#     Reset password
#     """
#     email = verify_password_reset_token(token=body.token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user = crud.get_user_by_email(session=session, email=email)
#     if not user:
#         raise HTTPException(status_code=404, detail="The user with this email does not exist in the system.")
#     elif not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     hashed_password = get_password_hash(password=body.new_password)
#     user.hashed_password = hashed_password
#     session.add(user)
#     session.commit()
#     return Message(message="Password updated successfully")
