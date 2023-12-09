from typing import List

from pydantic import BaseModel


class Comparison(BaseModel):
    sql_condition: str
    m_probability: float


class Settings(BaseModel):
    probability_two_random_records_match: float
    link_type: str
    comparisons: List[Comparison]


settings = Settings(
    probability_two_random_records_match=0.01,
    link_type="link_only",
    comparisons=[
        Comparison(sql_condition="name_l = name_r", m_probability=0.9),
        {
            "sql_condition": "name_l = name_r",
            "m_probability": 0.9,
        },
    ],
)

settings.comparisons

# [Comparison(sql_condition='name_l = name_r', m_probability=0.9),
#  Comparison(sql_condition='name_l = name_r', m_probability=0.9)]
