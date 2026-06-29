from .jd_parser import parse_job_description
from .resume_parser import parse_candidate
from .resume_ranker import rank_candidates

def run_pipeline(job_description, candidates):
    parsed_candidates = [parse_candidate(candidate) for candidate in candidates]
    rankings = rank_candidates(job_description, parsed_candidates)
    return rankings