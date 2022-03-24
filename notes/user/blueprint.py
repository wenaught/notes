"""This module defines the /user routes."""
from apiflask import APIBlueprint, abort

from notes.user.model import User, CreateUserSchema, LoginUserSchema, OutUserSchema, auth

user_blueprint = APIBlueprint("user", __name__,
                              url_prefix="/user",
                              tag={"name": "Users", "description": "User registration and login"})


@user_blueprint.post("")
@user_blueprint.input(CreateUserSchema,
                      example={"email": "email@example.com",
                               "username": "username",
                               "password": "secure_P4ss"}
                      )
@user_blueprint.output(OutUserSchema, 201, description="Newly created user")
def create_user(data: dict) -> User:
    """Create a User

    Create a new user.
    """
    user = User(**data)
    user.commit()
    return user


@user_blueprint.post("/login")
@user_blueprint.input(LoginUserSchema, example={"username": "username", "password": "secure_P4ss"})
@user_blueprint.output(OutUserSchema, description="User that just logged in")
@user_blueprint.doc(responses=[200, 401])
def login(data: dict) -> User:
    """Log in

    Log a user in.
    """
    user: User = User.find_one({"username": data["username"]})
    if user and user.compare_hash(data["password"]):
        return user
    abort(401, "Invalid user credentials")


@user_blueprint.get("")
@user_blueprint.auth_required(auth)
@user_blueprint.output(OutUserSchema, description="User currently logged in")
@user_blueprint.doc(responses=[200, 401])
def get_user() -> User:
    """Get Current User

    Get details of a user that's currently logged in.
    """
    return auth.current_user
