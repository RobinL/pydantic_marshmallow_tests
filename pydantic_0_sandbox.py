from pydantic import BaseModel, computed_field


class User(BaseModel):
    id: int
    name: str = "Jane Doe"

    @computed_field()
    @property
    def computed_field_1(self) -> str:
        return f"{self.name}-{self.id}"


# Example usage
user = User(id=123)  # Note: id should be an integer, not a string


user.model_computed_fields
user.model_dump_json()
print(user.model_json_schema())
