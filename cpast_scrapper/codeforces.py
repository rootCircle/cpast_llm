import cpast_scrapper.constant
import requests
import requests_cache
from pylatexenc.latex2text import LatexNodes2Text
from bs4 import BeautifulSoup

requests_cache.install_cache(
    cache_name='scrapper_cache', backend='sqlite', expire_after=18000
)


class CodeForces(BaseException):
    def __init__(self):
        pass

    def get_problems_by_code(
        self, contest_id: str, code: str
    ) -> cpast_scrapper.constant.ScrapeAPIResponse:
        response = requests.get(
            cpast_scrapper.constant.CODEFORCES_PREFIX.format(
                contest_id=contest_id, problem_code=code
            ),
            timeout=2.50,
        )
        if response.status_code == 200:
            response_soap = BeautifulSoup(response.content, 'html5lib')

            problem_components = response_soap.find('div', class_='problem-statement')  # pyright: ignore[reportCallIssue]

            if problem_components is None:
                raise CodeForcesError(
                    "Can't get the problem statement from the website"
                )

            try:
                input_spec_dom = problem_components.find(
                    'div',
                    class_='input-specification',  # pyright: ignore[reportCallIssue]
                )
                if input_spec_dom is not None:
                    input_format = LatexNodes2Text().latex_to_text(
                        input_spec_dom.text.replace('$$$', '')
                    )
                else:
                    input_format = ''

                statement_dom = problem_components.find('div', class_='')  # pyright: ignore[reportCallIssue]
                if statement_dom is not None:
                    statement = LatexNodes2Text().latex_to_text(
                        statement_dom.text.replace('$$$', '')
                    )
                else:
                    statement = ''

                constraints = ''

            except Exception as err:
                raise CodeForcesError(
                    "Can't extract Input Format and Problem Statements for the given question"
                ) from err

            return cpast_scrapper.constant.ScrapeAPIResponse(
                input_format=input_format,
                constraints=constraints,
                statement=statement,
            )
        else:
            raise CodeForcesError('Network Issue')


class CodeForcesError(Exception):
    def __init__(self, message):
        super().__init__(message)
