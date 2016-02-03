from enum import Enum

ErrorCodes = Enum("ErrorCodes",
        """
        NoError
        InternalServerError
        LoginFailed
        LoginCredentialsInvalid
        ConnectionRefused
        UserAlreadyExists
        UserDoesNotExist
        InvalidSession
        """,
        module=__name__
    )
