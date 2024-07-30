from fastapi import FastAPI, Request

from logic import get_characters

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return "OK"

@app.get("/search/{origin_name}")
def characters(origin_name: str, req: Request):
    filter_criteria = dict(req.query_params)
    return list(get_characters(origin_name, filter_criteria))
