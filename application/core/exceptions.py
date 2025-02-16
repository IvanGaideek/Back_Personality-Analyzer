from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='The user already exists')

IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail='Incorrect email or password')

TokenExpiredException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail='The token has expired')

TokenNoFound = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='The token has expired')

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='The token is not valid!')

NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='User ID not found')

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough rights!')
