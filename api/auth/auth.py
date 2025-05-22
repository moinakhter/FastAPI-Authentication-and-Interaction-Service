"""API authentication, represent checking for valid keys and generating new ones"""

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from utils.utils import (
    get_conf,
    get_sub_version_apis,
    get_version,
    request_api_version,
    validate_user_id,
)

token_ = APIKeyHeader(name="Authorization", auto_error=False)
sub_version_ = APIKeyHeader(name="SubVersion", auto_error=False)


def authenticate(
    token: str = Depends(token_), sub_version: str = Depends(sub_version_)
):
    """Authentication for APIs

    Args:
        token: User token for session.
        sub_version: Use for get the versions url.

    Returns:
        True if valid key, False otherwise
    """
    if token == get_conf("ADMIN_KEY"):
        is_valid, user_id, groups = True, -1, []
    else:
        is_valid, user_id, groups = validate_user_id(token=token, api_name="interact")
    # use your own code to apply authentication, request_api_version is validating token with dashboard api.
    if is_valid:
        version_data = get_sub_version_apis()
        parent_version = get_version()
        if (
            not version_data
            or parent_version not in version_data
            or sub_version not in version_data.get(parent_version)
        ):
            request_api_version(sub_version=sub_version, version_data=version_data)
        return is_valid, user_id, groups, sub_version
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "APIKey"},
        )
