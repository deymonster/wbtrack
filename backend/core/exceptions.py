from starlette.exceptions import HTTPException


class NotFound(HTTPException):
    def __init__(self, detail='Not found'):
        super().__init__(
            status_code=404,
            detail=detail
        )


class ValidationError(HTTPException):
    def __init__(self, detail='Bad request'):
        super().__init__(
            status_code=400,
            detail=detail
        )


class Conflict(HTTPException):
    def __init__(self, detail='Conflict'):
        super().__init__(
            status_code=409,
            detail=detail
        )


class PermissionDenied(HTTPException):
    def __init__(self, detail='Permission denied'):
        super().__init__(
            status_code=403,
            detail=detail
        )


class APIError(HTTPException):
    def __init__(self, detail='Internal server error'):
        super().__init__(
            status_code=500,
            detail=detail
        )


class NotAuthenticated(HTTPException):
    def __init__(self, detail='Not authenticated'):
        super().__init__(
            status_code=401,
            detail=detail
        )
