def refresh_access_token(refresh_token):

    username = verify_token(refresh_token, token_type="refresh")

    if not username:
        return None

    access_token = create_token(username, token_type="access")

    return access_token