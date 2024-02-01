import cpast_scrapper.constant
import requests
import requests_cache
from pylatexenc.latex2text import LatexNodes2Text

requests_cache.install_cache(
    cache_name="scrapper_cache", backend="sqlite", expire_after=18000
)


class CodeChef(BaseException):
    def __init__(self):
        pass

    def get_problems_by_code(code: str) -> cpast_scrapper.constant.ScrapeAPIResponse:
        response = requests.get(
            cpast_scrapper.constant.CODECHEF_PREFIX.format(problem_code=code),
            timeout=2.50,
        )
        if response.status_code == 200:
            response = response.json()
            problem_components: dict | None = response.get("problemComponents")
            if problem_components is None:
                raise CodeChefError("Problem not found!")

            input_format = LatexNodes2Text().latex_to_text(
                problem_components.get("inputFormat")
            )
            constraints = LatexNodes2Text().latex_to_text(
                problem_components.get("constraints")
            )
            statement = LatexNodes2Text().latex_to_text(
                problem_components.get("statement")
            )

            return cpast_scrapper.constant.ScrapeAPIResponse(
                input_format=input_format,
                constraints=constraints,
                statement=statement,
            )
        else:
            raise CodeChefError("Network Issue")


class CodeChefError(Exception):
    def __init__(self, message):
        super().__init__(message)
