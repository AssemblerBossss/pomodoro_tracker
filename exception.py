class UserNotFoundException(Exception):
    message = "User not found"


class UserUnCorrectPasswordException(Exception):
    message = "Wrong password"
