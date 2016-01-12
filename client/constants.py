from enum import Enum

ErrorCodes = Enum("ErrorCodes",
        """
        NoError
        InternalServerError
        LoginFailed
        LoginCredentialsInvalid
        ConnectionRefused
        UserAlreadyExists
        """,
        module=__name__
    )
