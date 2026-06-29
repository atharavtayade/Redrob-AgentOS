from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class RankRequest(BaseModel):
    job_description: str
    candidates: list


@app.post("/rank")
async def rank_candidates(request: RankRequest):
    return run_pipeline(
        request.job_description, 
        request.candidates
    )


from services.ranking_pipeline import run_pipeline
