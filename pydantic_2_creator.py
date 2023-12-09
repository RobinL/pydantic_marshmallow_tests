from enum import Enum

from pydantic import BaseModel, validator


class LinkType(str, Enum):
    dedupe_only = "dedupe_only"
    link_and_dedupe = "link_and_dedupe"
    link_only = "link_only"


class ComparisonCreator(BaseModel):
    sql: str = None  # Attribute to store the SQL

    @classmethod
    def get_sql(cls, dialect: str):
        return "sql " + dialect


class Settings(BaseModel):
    link_type: LinkType
    comparison: ComparisonCreator
    dialect: str = None  # Optional attribute to store the dialect

    def hydrate_comparison(self):
        if self.dialect:
            self.comparison.sql = ComparisonCreator.get_sql(self.dialect)

    @validator("dialect", allow_reuse=True)
    def check_dialect(cls, v, values):
        if v and "comparison" in values:
            values["comparison"].sql = ComparisonCreator.get_sql(v)
        return v


# Example usage
s = Settings(
    link_type="link_only", comparison=ComparisonCreator(), dialect="some_dialect"
)
s.hydrate_comparison()
print(s.comparison.sql)  # This should now print the hydrated SQL
s.model_dump_json()
