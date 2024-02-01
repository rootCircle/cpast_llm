from pydantic import BaseModel


CODECHEF_PREFIX = (
    "https://www.codechef.com/api/contests/PRACTICE/problems/{problem_code}"
)
CODEFORCES_PREFIX = "https://codeforces.com/contest/{contest_id}/problem/{problem_code}"


class ScrapeAPIResponse(BaseModel):
    input_format: str
    constraints: str
    statement: str
