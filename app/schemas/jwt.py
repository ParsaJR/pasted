from pydantic import BaseModel


# "Token" is a schema that adheres the OAuth2 specification for auth response.
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
