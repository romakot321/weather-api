from app.services.auth import fastapi_users

get_current_user = fastapi_users.current_user(active=True)

