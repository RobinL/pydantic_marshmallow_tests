# How would constructing settings actually work in Splink?
from dataclasses import dataclass
from typing import List


class LinkType(str):
    dedupe_only = "dedupe_only"
    link_and_dedupe = "link_and_dedupe"
    link_only = "link_only"


@dataclass
class ComparisonLevel:
    sql: str


@dataclass
class Comparison:
    name: str
    comparison_levels: List[ComparisonLevel]


@dataclass
class UserSettings:
    probability_two_random_records_match: float
    link_type: LinkType
    comparisons: List[Comparison]


class ExactMatch(Comparison):
    pass


# This can be a mix of dicts and classes?
# Or if we get the schma right should it always be classes?
# (But then it would potentially mix undialected and dialected?)
settings = UserSettings(
    probability_two_random_records_match=0.01,
    link_type=LinkType.link_only,
    comparisons=[
        ExactMatch("surname"),
        Comparison(
            "name",
            [
                ComparisonLevel(sql="name_l = name_r"),
                ComparisonLevel(sql="name_l is NULL"),
                ComparisonLevel(sql="else"),
            ],
        ),
    ],
)

Linker(settings)
