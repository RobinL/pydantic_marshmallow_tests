from typing import List, Optional, Union

from pydantic import BaseModel


class Comparison(BaseModel):
    sql_condition: str
    m_probability: Optional[float]


class ComparisonCreator:
    def get_comparison(self, dialect: str):
        pass


class ExactMatch(ComparisonCreator):
    def __init__(self, name: str, m_probability: None) -> None:
        self.name = name
        self.m_probability = m_probability

    def get_comparison(self, dialect: str):
        comparison_kwargs = {
            "sql_condition": f"{self.name}_l = {self.name}_r ({dialect})"
        }
        if self.m_probability is not None:
            comparison_kwargs["m_probability"] = self.m_probability
        return Comparison(**comparison_kwargs)


class Settings(BaseModel):
    _dialect: Optional[str] = None
    comparisons: List[Union[Comparison, ComparisonCreator]]

    class Config:
        arbitrary_types_allowed = True

    @property
    def dialect(self) -> Optional[str]:
        return self._dialect

    @dialect.setter
    def dialect(self, value: Optional[str]) -> None:
        self._dialect = value
        if value is not None:
            for i, c in enumerate(self.comparisons):
                if isinstance(c, ComparisonCreator):
                    self.comparisons[i] = c.get_comparison(value)


settings = Settings(
    comparisons=[
        Comparison(sql_condition="name_l = name_r", m_probability=0.9),
        {
            "sql_condition": "name_l = name_r",
            "m_probability": 0.9,
        },
        ExactMatch(name="surname", m_probability=0.9),
    ],
)


# print(settings.model_dump_json(indent=4))

settings.dialect = "duckdb"

print(settings.model_dump_json(indent=4))

settings.comparisons[0].m_probability = "hi"
settings.model_validate(settings.model_dump())
