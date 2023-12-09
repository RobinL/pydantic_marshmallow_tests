from typing import Union

from pydantic import BaseModel


class Comparison(BaseModel):
    sql_condition: str
    m_probability: float


class ComparisonCreator(BaseModel):
    @classmethod
    def get_comparison(cls, dialect: str):
        return Comparison(sql_condition="sql " + dialect, m_probability=0.9)


class Settings(BaseModel):
    comparison: Union[Comparison, ComparisonCreator]
    dialect: Union[str, None] = None

    def hydrate_comparison(self, dialect: str):
        self.dialect = dialect

        self.comparison = ComparisonCreator.get_comparison(self.dialect)


s = Settings(
    dialect="some_dialect",
    comparison=ComparisonCreator(),
)
s.model_dump_json()
s.hydrate_comparison("duckdb")
s.model_dump_json()
