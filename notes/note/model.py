"""This module defines the models and schemas used by the 'note' entities of the API."""
import os

from marshmallow import validates
from marshmallow.validate import Length
from umongo import Document, fields, post_load, ValidationError
from umongo.frameworks import PyMongoInstance, MongoMockInstance

from notes.user.model import auth

note_umongo_instance = PyMongoInstance() if not os.getenv("MOCK_MONGO") else MongoMockInstance()


@note_umongo_instance.register
class Note(Document):
    """A MongoDB model for the 'note' document."""
    username = fields.StrField(required=True)
    title = fields.StrField(
        required=True,
        validate=Length(min=1, max=20),
        metadata={
            "title": "Note title",
            "description": "Title of the note"
        }
    )
    text = fields.StrField(
        required=True,
        validate=Length(min=1),
        metadata={
            "title": "Note text",
            "description": "Text of the note"
        }
    )
    added_timestamp = fields.DateTimeField(
        metadata={
            "title": "Time of creation",
            "description": "Timestamp added to the note at the time of creation"
        }
    )
    modified_timestamp = fields.DateTimeField(
        metadata={
            "title": "Time of last modification",
            "description": "Timestamp of the last modification"
        }
    )

    class Meta:
        collection_name = "notes"
        indexes = ("title", "text")


NoteSchema = Note.schema.as_marshmallow_schema()


class InNoteSchema(NoteSchema):
    """A schema that defines input fields for a 'note' document."""

    def __init__(self, *args, update: bool = False, **kwargs):
        """Add an 'update' field to object instance for usage in validation.

        :param update: whether the schema is used in 'update' operation.
        """
        NoteSchema.__init__(self, *args, **kwargs)
        self.update = update

    @post_load
    def add_username(self, data: dict, **kwargs) -> dict:
        """Update the data with current user's username after loading.

        :param data: data loaded with this schema.
        :return: updated data.
        """
        data["username"] = auth.current_user["username"]
        return data

    @validates("title")
    def unique_title(self, value: str):
        """Validate that title is unique for user.

        :param value: value of the field.
        :raise: marshmallow.ValidationError if a note with given title already exists for user.
        """
        if Note.find_one({"title": value, "username": auth.current_user["username"]}) and not self.update:
            raise ValidationError("Title must be unique")

    class Meta:
        fields = ("title", "text")


class QueryNoteSchema(NoteSchema):
    title = fields.StrField(
        validate=Length(max=20),
        metadata={
            "title": "Note title",
            "description": "Title of the note"
        }
    )
    text = fields.StrField(
        metadata={
            "title": "Note text",
            "description": "Text of the note"
        }
    )

    class Meta:
        fields = ("title", "text")



class OutNoteSchema(NoteSchema):
    """A schema that defines output fields for a 'note' document."""

    class Meta:
        fields = ("title", "added_timestamp", "modified_timestamp", "text")
