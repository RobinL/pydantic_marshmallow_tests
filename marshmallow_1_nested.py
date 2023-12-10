# Nested example from
# https://www.augmentedmind.de/2020/10/25/marshmallow-vs-pydantic-python/

import json
from dataclasses import dataclass
from typing import List, Optional

from marshmallow import Schema, fields, post_load, validate


@dataclass
class Book:
    title: str
    isbn: str


@dataclass
class User:
    email: str
    books: Optional[List[Book]] = None


def validate_isbn(isbn: str) -> None:
    """Validates the isbn with some code (omitted), raise marshmallow.ValidationError if validation did not pass"""


class BookSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(max=120))
    isbn = fields.String(required=True, validate=validate_isbn)

    @post_load
    def make_obj(self, data, **kwargs):  # note: method name is arbitrary
        return Book(**data)


class UserSchema(Schema):
    email = fields.Email(required=True)
    books = fields.Nested(BookSchema, many=True, required=False)

    @post_load
    def make_obj(self, data, **kwargs):  # note: method name is arbitrary
        return User(**data)


raw_data_str = """{
    "email": "foo@bar.com",
    "books": [
        {"title": "Hitchhikers Guide to the Galaxy", "isbn": "123456789"},
        {"title": "Clean Coder", "isbn": "987654321"}
    ]
}"""
json_data = json.loads(raw_data_str)

schema = UserSchema()
# Post load needs to be implemented for this to work
user = schema.load(json_data)
user
