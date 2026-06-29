import re


def parse_job_description(job_description: str) -> dict:
    """Parse a job description and extract title, skills, and keywords.

    Args:
        job_description: The raw job description text to parse.

    Returns:
        A dictionary containing the extracted job title as a string, 
        list of skills found in the description, and list of relevant keywords.
    """    
    return {"title": "", "skills": [], "keywords": []}
