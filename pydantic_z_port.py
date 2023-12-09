from typing import Optional

from pydantic import BaseModel


class ConfigItem(BaseModel):
    name: str
    value: str
    port: Optional[int] = None

    # @model_validator(mode="before")
    # def check_port(cls, v, values):
    #     if "port" not in v or v["port"] is None:
    #         raise ValueError("Port is not configured yet.")
    #     return v


data = {"name": "MySQL", "value": "mysql://user:pass@localhost/db", "a": 1}
config = ConfigItem(**data)

print(config.model_dump_json(indent=2))


from typing import Optional

from pydantic import BaseModel


class ConfigItem(BaseModel):
    name: str
    value: str
    port: Optional[int] = None

    class Config:
        validate_assignment = True


config = ConfigItem(name="MySQL", value="mysql:", port=3306)
config.port = "hello"

print(config.model_dump_json(indent=2))
