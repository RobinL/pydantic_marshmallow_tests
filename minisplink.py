# This ignores the 'creator' part of Splink 4.

# We only use pydantic and validate
# after the creators have been 'dialected'

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, model_validator


class LinkType(str, Enum):
    dedupe_only = "dedupe_only"
    link_and_dedupe = "link_and_dedupe"
    link_only = "link_only"


class ComparisonLevel(BaseModel):
    sql_condition: str
    label_for_charts: Optional[str] = None
    tf_adjustment_column: Optional[str] = None

    # How to set 'dependent' default value i.e. if tf_adjustment_column is set
    # perhaps all tf options need to be a class?
    tf_adjustment_weight: Optional[float] = None
    tf_minimum_u_value: Optional[float] = None
    is_null_level: Optional[bool] = None

    @model_validator(mode="after")
    def check_dialect(cls, v, values):
        if v.tf_adjustment_column is not None:
            if v.tf_adjustment_weight is None:
                v.tf_adjustment_weight = 1.0
        return v

    @property
    def columns_used(self):
        return self.sql_condition.upper()


level_match = ComparisonLevel(
    sql_condition="name_l = name_r",
    label_for_charts="Exact match on name",
)

level_else = ComparisonLevel(
    sql_condition="else",
    label_for_charts="All others",
)


class Comparison(BaseModel):
    output_column_name: str
    comparison_levels: list[ComparisonLevel]
    comparison_description: Optional[str] = None

    def model_dump(self):
        return {k: getattr(self, k) for k in self.model_fields_set}


comparison_1 = Comparison(
    output_column_name="name_match",
    comparison_levels=[level_match, level_else],
    comparison_description="This is a comparison",
)

comparison_2 = Comparison(
    output_column_name="dob_match",
    comparison_levels=[
        ComparisonLevel(sql_condition="dob_l is NULL"),
        ComparisonLevel(sql_condition="dob_l = dob_r"),
    ],
    comparison_description="A second comparison",
)


class Settings(BaseModel):
    probability_two_random_records_match: float
    link_type: LinkType
    comparisons: Optional[List[Comparison]]
    retain_intermediate_calculation_columns: bool = False
    retain_matching_columns: bool = True
    max_iterations: int = 10
    em_convergence: float = 0.0001


settings = Settings(
    probability_two_random_records_match=0.01,
    link_type="link_only2",
    comparisons=[comparison_1, comparison_2],
)

s = settings.model_dump(exclude_unset=True)
settings.model_dump_json(indent=4)

settings.comparisons[0].comparison_levels[0].columns_used
