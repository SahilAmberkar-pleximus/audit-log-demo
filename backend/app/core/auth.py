from pydantic import BaseModel

class CurrentUser(BaseModel):
    guid: str
    username: str
    full_name: str 
    email: str | None = None



# Temporary demo identity

def get_current_user():
    return CurrentUser(
        guid="demo-user-001",
        username="demo.admin",
        full_name="Demo Administrator",
        email="admin@example.com",
    )