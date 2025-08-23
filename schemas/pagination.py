from pydantic import BaseModel
from typing import List, Generic, TypeVar

from pydantic.v1.generics import GenericModel

T = TypeVar("T")

class Page(BaseModel):
    page: int
    size: int
    total: int

class PaginatedResponse(GenericModel, Generic[T]):
    data: List[T]
    page: Page