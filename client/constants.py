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
        ServerNotConfigured
        ThriftError
        """,
        module=__name__
    )
