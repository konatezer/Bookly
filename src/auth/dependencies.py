from fastapi import HTTPException, Request, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .utils import decode_token
from src.db.redis import token_in_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
from typing import List, Any
from .models import User

user_servive = UserService()


class TokenBearer(HTTPBearer):

    def __init(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials
        token_data = decode_token(token)

        # logging.debug(f"token_data: {token_data}")

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "Error": "this token is invalid or expired",
                    "resolustion": "Please get a nev token",
                },
            )

        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "Error": "this token is invalid or has been revoked",
                    "resolution": "Please get a new token",
                },
            )

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:

        token_data = decode_token(token)
        return token_data is not None

    def verify_token_data(selft, token_data):
        if token_data and token_data["refresh"]:
            raise NotImplementedError("Please override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(selft, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(selft, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an refresh token",
            )


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_details["user"]["email"]
    user = await user_servive.get_user_by_email(user_email, session)

    return user




class RoleChecker:
    def __init__(self, allowed_roles: List[str] ) -> None:
        
        self.allowd_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        
        
        if current_user.role in self.allowd_roles:
            return True
        
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action"
        )