from typing import Optional, Literal

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from logic import get_characters

app = FastAPI()


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='/docs#/default/characters_search__origin_name__get')


@app.get("/healthcheck")
async def healthcheck():
    return "OK"


@app.get("/search/{origin_name}")
async def characters(
        origin_name: str,
        name: Optional[str] = None,
        status: Optional[Literal["alive", "dead", "unknown"]] = None,
        species: Optional[str] = None,
        type: Optional[str] = None,
        gender: Optional[Literal["female", "male", "genderless", "unknown"]] = None
):
    filter_criteria = {
        "name": name,
        "status": status,
        "species": species,
        "type": type,
        "gender": gender
    }

    filter_criteria = {k: v for k, v in filter_criteria.items() if v is not None}
    return list(get_characters(origin_name, filter_criteria))
