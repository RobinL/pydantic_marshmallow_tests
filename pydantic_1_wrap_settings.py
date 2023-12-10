from enum import Enum
from typing import List

from pydantic import BaseModel


class LinkType(str, Enum):
    dedupe_only = "dedupe_only"
    link_and_dedupe = "link_and_dedupe"
    link_only = "link_only"


class Comparison(BaseModel):
    sql_condition: str
    m_probability: float


class Settings(BaseModel):
    probability_two_random_records_match: float
    link_type: LinkType
    comparisons: List[Comparison]


# Example usage
settings = {
    "probability_two_random_records_match": 0.01,
    "link_type": "dedupe_only",
    "comparisons": [
        {
            "sql_condition": "name_l = name_r",
            "m_probability": 0.9,
        },
        {
            "sql_condition": "name_l is NULL",
            "m_probability": 0.3,
        },
    ],
}

validated_settings = Settings(**settings)

settings = Settings(
    probability_two_random_records_match=0.01,
    link_type=LinkType.link_only,
    comparisons=[
        Comparison(sql_condition="name_l = name_r", m_probability=0.9),
    ],
)

# How does this work with undialected?  i.e. our ComparisonCreator?
settings.comparisons
print(settings.model_json_schema())
