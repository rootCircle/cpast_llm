import cpast_scrapper.constant
import requests
import requests_cache
from pylatexenc.latex2text import LatexNodes2Text
from bs4 import BeautifulSoup

requests_cache.install_cache(
    cache_name="scrapper_cache", backend="sqlite", expire_after=18000
)


class CodeForces(BaseException):
    def __init__(self):
        pass

    def get_problems_by_code(
        contest_id: str, code: str
    ) -> cpast_scrapper.constant.ScrapeAPIResponse:
        response = requests.get(
            cpast_scrapper.constant.CODEFORCES_PREFIX.format(
                contest_id=contest_id, problem_code=code
            ),
            timeout=2.50,
        )
        if response.status_code == 200:
            response_soap = BeautifulSoup(response.content, "html5lib")

            problem_components = response_soap.find(
                "div", {"class": "problem-statement"}
            )

            try:
                input_format = LatexNodes2Text().latex_to_text(
                    problem_components.find(
                        "div", {"class": "input-specification"}
                    ).text.replace("$$$", "")
                )
                statement = LatexNodes2Text().latex_to_text(
                    problem_components.find("div", {"class": ""}).text.replace(
                        "$$$", ""
                    )
                )
                constraints = ""

            except Exception:
                raise CodeForcesError(
                    "Can't extract Input Format and Problem Statements for the given question"
                )

            return cpast_scrapper.constant.ScrapeAPIResponse(
                input_format=input_format,
                constraints=constraints,
                statement=statement,
            )
        else:
            raise CodeForcesError("Network Issue")


class CodeForcesError(Exception):
    def __init__(self, message):
        super().__init__(message)
