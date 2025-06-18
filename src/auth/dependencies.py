import logging
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .utils import decode_token
from src.db.redis import token_in_blocklist


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
