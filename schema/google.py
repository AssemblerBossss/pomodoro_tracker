from pydantic import  BaseModel, EmailStr

class  GoogleUserData(BaseModel):
    """Represents user data retrieved from Google OAuth2 API.

    Attributes:
        id: Google user unique identifier
        name: User's full name
        email: User's email address (validated format)
        verified_email: Indicates if the email address has been verified by Google
    """
    id: int
    name: str
    email: EmailStr
    verified_email: bool
    access_token: str
