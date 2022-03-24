"""This module defines the models and schemas used by the 'user' entities of the API."""
import os
import re

from flask import current_app
from jwt import encode, decode, InvalidTokenError
from apiflask import HTTPTokenAuth
from marshmallow import validates
from marshmallow.validate import Length, Email
from umongo import Document, fields, ValidationError, post_load, post_dump
from umongo.frameworks import PyMongoInstance, MongoMockInstance
from werkzeug.security import generate_password_hash, check_password_hash

user_umongo_instance = PyMongoInstance() if not os.getenv("MOCK_MONGO") else MongoMockInstance()


@user_umongo_instance.register
class User(Document):
    """A MongoDB model for the 'user' document."""
    username: str = fields.StrField(
        required=True,
        unique=True,
        validate=Length(min=5, max=15),
        metadata={
            "title": "Username",
            "description": "Username used to log in"
        }
    )
    email: str = fields.StrField(
        required=True,
        unique=True,
        validate=Email(),
        metadata={
            "title": "User email",
            "description": "Email used to sign up"
        }
    )
    password_hash: str = fields.StrField()

    class Meta:
        collection_name = "users"

    def compare_hash(self, password: str) -> bool:
        """Validate given password against stored hash value.

        :param password: password to validate.
        :return: whether password hashes match.
        """
        return check_password_hash(self.password_hash, password)


UserSchema = User.schema.as_marshmallow_schema()


class CreateUserSchema(UserSchema):
    """A schema that defines input fields for a new 'user' document."""
    password = fields.StrField(
        required=True,
        metadata={
            "title": "User password",
            "description": "Password used to log in; must be at least 6 characters long, include lower- and "
                           "uppercase letters, digits, and special symbols (@$!#%*?&_)"}
    )

    @validates("password")
    def validate_password(self, password: str) -> None:
        """Validate given password against complexity constraints.

        :param password: given password.
        :raise: marshmallow.ValidationError when password isn't complex enough.
        """
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!#%*?&_]{6,20}$")
        if not re.search(pattern, password):
            raise ValidationError("Password not matching minimum complexity requirements.")

    @post_load
    def create_hash(self, data: dict, **kwargs) -> dict:
        """Create a hash of the password to store.

        :param data: dictionary of values passed in.
        :return: processed input dictionary.
        """
        data["password_hash"] = generate_password_hash(data.pop("password"))
        return data

    class Meta:
        fields = ("email", "username", "password")


class LoginUserSchema(UserSchema):
    """A schema that defines input fields for a user logging in."""
    password = fields.StrField(
        required=True,
        metadata={
            "title": "User password",
            "description": "Password used to log in"}
    )

    class Meta:
        fields = ("username", "password")


class OutUserSchema(UserSchema):
    """A schema that defines output fields for a created user."""
    token = fields.StrField(
        metadata={
            "title": "Authentication token",
            "description": "Token used to authenticate user"
        }
    )

    @post_dump
    def create_token(self, data: dict, **kwargs):
        token = encode(data, current_app.secret_key)
        data["token"] = token
        return data

    class Meta:
        fields = ("email", "username", "token")


auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token: str) -> None | User:
    """Verify that user identity can be restored from token.

    :param token: an HS256-encoded payload.
    :return: either a User object, or None in case of decoding failure.
    """
    try:
        return User.find_one(decode(token, current_app.secret_key, algorithms=["HS256"]))
    except InvalidTokenError:
        return
