"""This module defines the /note routes."""
import datetime

from apiflask import APIBlueprint, abort

from notes.note.model import Note, InNoteSchema, OutNoteSchema, QueryNoteSchema
from notes.user.model import auth

note_blueprint = APIBlueprint("notes", __name__,
                              url_prefix="/note",
                              tag={"name": "Notes", "description": "Interaction with the notes"})


@note_blueprint.post("")
@note_blueprint.auth_required(auth)
@note_blueprint.input(InNoteSchema)
@note_blueprint.output(OutNoteSchema, 201, description="Newly created note")
def post_note(data: dict) -> Note:
    """Post a Note

    Post a note with given title and text.
    """
    note = Note(**data)
    note.added_timestamp = note.modified_timestamp = datetime.datetime.now()
    note.commit()
    return note


@note_blueprint.get("/<string:title>")
@note_blueprint.auth_required(auth)
@note_blueprint.output(OutNoteSchema)
@note_blueprint.doc(responses=[200, 404])
def get_note(title: str) -> Note:
    """Get a Note

    Get a note by title.
    """
    note = Note.find_one({"title": title,
                          "username": auth.current_user["username"]})
    if not note:
        abort(404)
    return note


@note_blueprint.put("/<string:title>")
@note_blueprint.auth_required(auth)
@note_blueprint.input(InNoteSchema(partial=True, update=True))
@note_blueprint.output(OutNoteSchema)
@note_blueprint.doc(responses=[200, 404])
def put_note(title: str, data: dict) -> Note:
    """Update a Note

    Update a note by title.
    """
    note = Note.find_one({"title": title,
                          "username": auth.current_user["username"]})
    if not note:
        abort(404)
    note.update(data)
    note.modified_timestamp = datetime.datetime.now()
    note.commit()
    return note


@note_blueprint.delete("/<string:title>")
@note_blueprint.auth_required(auth)
@note_blueprint.output({}, 204)
@note_blueprint.doc(responses=[204, 404])
def delete_note(title: str) -> None:
    """Delete a Note

    Delete a note by title.
    """
    note = Note.find_one({"title": title,
                          "username": auth.current_user["username"]})
    if not note:
        abort(404)
    note.delete()


@note_blueprint.get("")
@note_blueprint.auth_required(auth)
@note_blueprint.input(QueryNoteSchema, location="query")
@note_blueprint.output(OutNoteSchema(many=True))
def get_notes(query: dict) -> list[Note]:
    """Get All Notes

    Get all notes filtered with query.
    """
    query.update({"username": auth.current_user["username"]})
    return list(Note.find(query))
