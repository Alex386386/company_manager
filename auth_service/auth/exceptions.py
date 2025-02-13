from fastapi import status, HTTPException

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
expired_token_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Refresh token expired",
    headers={"WWW-Authenticate": "Bearer"},
)
incorrect_data_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
