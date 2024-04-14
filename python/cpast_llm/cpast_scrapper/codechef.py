import cpast_llm.cpast_utils.scrape_models
import requests
import requests_cache
from pylatexenc.latex2text import LatexNodes2Text

requests_cache.install_cache(
    cache_name=cpast_llm.cpast_utils.scrape_models.SCRAPPER_CACHE_FILENAME,
    backend='sqlite',
    expire_after=18000,
)


class CodeChef(BaseException):
    def __init__(self):
        pass

    def get_problems_by_code(
        self, code: str
    ) -> cpast_llm.cpast_utils.scrape_models.ScrapeAPIResponse:
        try:
            response = requests.get(
                cpast_llm.cpast_utils.scrape_models.CODECHEF_PREFIX.format(
                    problem_code=code
                ),
                timeout=2.50,
            )
        except requests.exceptions.ReadTimeout as err:
            raise CodeChefError('Network Issue') from err

        if response.status_code == 200:
            response = response.json()
            problem_components: dict | None = response.get('problemComponents')
            if problem_components is None:
                raise CodeChefError('Problem not found!')

            input_format = LatexNodes2Text().latex_to_text(
                problem_components.get('inputFormat')
            )
            constraints = LatexNodes2Text().latex_to_text(
                problem_components.get('constraints')
            )
            statement = LatexNodes2Text().latex_to_text(
                problem_components.get('statement')
            )

            return cpast_llm.cpast_utils.scrape_models.ScrapeAPIResponse(
                input_format=input_format,
                constraints=constraints,
                statement=statement,
            )
        else:
            raise CodeChefError('Network Issue')


class CodeChefError(Exception):
    def __init__(self, message):
        super().__init__(message)
