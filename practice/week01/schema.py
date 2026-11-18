"""Kiem tra ket qua model bang Pydantic.

Neu model tra sai category/priority, hoac thieu next_action,
thi Pydantic se bao loi (schema khong hop le).
"""

from typing import Literal
from pydantic import BaseModel, Field


# Chi cho phep dung 4 category va 3 priority nay
Category = Literal["Bug", "Feature", "Question", "Risk"]
Priority = Literal["P1", "P2", "P3"]


class IssuePrediction(BaseModel):
    """Mot ket qua phan loai hop le."""

    category: Category
    priority: Priority
    next_action: str = Field(min_length=1)


def parse_prediction(data: dict) -> IssuePrediction:
    """Chuyen dict thanh IssuePrediction. Sai thi raise ValidationError."""
    return IssuePrediction.model_validate(data)
