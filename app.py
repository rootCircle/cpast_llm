import cpast_llm.prompt as prompt
import cpast_llm.chat as chat
import cpast_scrapper.codeforces as codeforces
import cpast_scrapper.codechef as codechef
import cpast_scrapper.constant
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.pydantic_v1 import SecretStr
import cpast_utils.env_util
import cpast_lib

load_dotenv()
app = FastAPI()

GOOGLE_API_KEY: SecretStr = cpast_utils.env_util.get_env_var('GOOGLE_API_KEY')

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/api/test')
async def test():
    return 'Hello World!'


class Request(BaseModel):
    real_input_format: str
    real_constraints: str


class CpastLibResponse(BaseModel):
    Ok: str | None = None
    Err: str | None = None


class Response(BaseModel):
    clex_lang: str
    generated_response: CpastLibResponse


@app.post('/api/llm/generate')
async def generate(request: Request) -> Response:
    return generate_response(request.real_input_format, request.real_constraints)


@app.get('/api/code/codechef/{problem_code}')
async def get_codechef_problem(
    problem_code: str,
) -> cpast_scrapper.constant.ScrapeAPIResponse:
    return codechef.CodeChef().get_problems_by_code(problem_code)


@app.get('/api/code/codeforces/{contest_id}/{problem_code}')
async def get_codeforces_problem(
    contest_id: str, problem_code: str
) -> cpast_scrapper.constant.ScrapeAPIResponse:
    return codeforces.CodeForces().get_problems_by_code(contest_id, problem_code)


def generate_response(real_input_format: str, real_constraints: str) -> Response:
    chat_model = chat.ClexChatModel(GOOGLE_API_KEY, './.langchain.db')
    prompt_content = prompt.ClexPromptGenerator()
    lang_specs = prompt_content.get_lang_specs(path='./clex.spec.md')

    _real_input_format = """
    First line will contain T, number of test cases. Then the test cases follow.
    The first line of each test case contains two integers N and K.
    The second line contains the string S.
    """

    _real_constraints = """
    1≤T≤1000
    1≤N≤10^6
    1≤K≤10^6
    S consists of 0 and 1 only.
    The sum of N and K over all test cases won't exceed 5⋅10^6.
    """

    formatted_prompt_input = {
        'real_input_format': real_input_format,
        'real_constraints': real_constraints,
        'lang_specs': lang_specs,
    }

    response = chat_model.call_model(
        prompt_content.get_dynamic_prompt(), input=formatted_prompt_input
    )

    generated_testcases: dict = cpast_lib.generate(  # pyright: ignore[reportAttributeAccessIssue]
        response
    )

    return Response(
        clex_lang=response,
        generated_response=CpastLibResponse(
            Ok=generated_testcases.get('Ok'), Err=generated_testcases.get('Err')
        ),
    )
