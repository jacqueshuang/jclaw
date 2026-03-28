from fastapi import Header, HTTPException, status


API_KEY_HEADER = "x-api-key"


def require_api_key(x_api_key: str | None = Header(default=None)) -> str:
    if x_api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API key")

    return x_api_key
