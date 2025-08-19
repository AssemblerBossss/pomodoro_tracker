class UserNotFoundException(Exception):
    detail = "User not found"


class UserUnCorrectPasswordException(Exception):
    detail = "Wrong password"


class TokenExpiredException(Exception):
    detail = "Token expired"


class InvalidTokenException(Exception):
    detail = "Invalid token"
