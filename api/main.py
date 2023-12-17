from api.good_dates import good_dates

from fastapi import FastAPI

from api.model import GoodDateRequest

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/good-dates/", response_model=dict)
async def get_good_dates(data: GoodDateRequest):
    dates = good_dates(
        year=data.year,
        birth_date=data.birth_date,
        match_on_single_digit=data.match_on_single_digit,
    )

    return {"dates": dates}
