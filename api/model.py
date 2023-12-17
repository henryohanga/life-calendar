from pydantic import BaseModel


class GoodDateRequest(BaseModel):
    year: int
    birth_date: str
    match_on_single_digit: bool = True
