from typing import Union
import cpast_llm.cpast_prompt.prompt as prompt
import cpast_llm.cpast_prompt.chat as chat
import cpast_llm.cpast_scrapper.codeforces as codeforces
import cpast_llm.cpast_scrapper.codechef as codechef
import cpast_llm.cpast_utils.models
import cpast_llm.cpast_utils.scrape_models
import cpast_llm.cpast_db.clex_cache as clex_cache
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.pydantic_v1 import SecretStr
import cpast_llm.cpast_utils.env_util
import cpast_llm.cpast_utils.models as CModels
import cpast_llm.cpast_lib

load_dotenv()
app = FastAPI()

GOOGLE_API_KEY: SecretStr = cpast_llm.cpast_utils.env_util.get_env_var('GOOGLE_API_KEY')

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


@app.post('/api/llm/generate')
async def llm_generate(request: CModels.LLMRequest) -> CModels.LLMResponse:
    clex: str = generate_response(request.input_format, request.constraints)

    generated_testcases: dict = cpast_llm.cpast_lib.generate(  # pyright: ignore[reportAttributeAccessIssue]
        clex
    )

    return CModels.LLMResponse(
        clex_lang=clex,
        generated_response=CModels.CpastLibResponse(
            Ok=generated_testcases.get('Ok'), Err=generated_testcases.get('Err')
        ),
    )


@app.post('/api/llm/clex')
async def llm_clex(request: CModels.LLMRequest) -> CModels.LLMGenerateResponse:
    return CModels.LLMGenerateResponse(
        clex=generate_response(request.input_format, request.constraints)
    )


@app.post('/api/testcases/generate')
async def testcase_generate(
    request: CModels.TestcaseRequest,
) -> CModels.TestcaseResponse:
    testcases: CModels.TestcaseResponse = CModels.TestcaseResponse(testcases=[])
    for _ in range(request.iterations):
        generated_testcases: dict = cpast_llm.cpast_lib.generate(  # pyright: ignore[reportAttributeAccessIssue]
            request.clex
        )
        testcases.testcases.append(
            CModels.CpastLibResponse(
                Ok=generated_testcases.get('Ok'), Err=generated_testcases.get('Err')
            )
        )

    return testcases


@app.get('/api/code/codechef/{problem_code}')
async def get_codechef_problem(
    problem_code: str,
) -> cpast_llm.cpast_utils.scrape_models.ScrapeAPIResponse:
    return codechef.CodeChef().get_problems_by_code(problem_code)


@app.get('/api/code/codeforces/{contest_id}/{problem_code}')
async def get_codeforces_problem(
    contest_id: str, problem_code: str
) -> cpast_llm.cpast_utils.scrape_models.ScrapeAPIResponse:
    return codeforces.CodeForces().get_problems_by_code(contest_id, problem_code)


@app.get('/api/testcases/codechef/{problem_code}')
async def generate_testcase_codechef(
    problem_code: str,
) -> CModels.LLMResponse:
    scrape_response: cpast_llm.cpast_utils.scrape_models.ScrapeAPIResponse = (
        codechef.CodeChef().get_problems_by_code(problem_code)
    )
    clex: str = generate_response(
        scrape_response.input_format,
        scrape_response.constraints,
        'codechef',
        problem_code,
    )

    generated_testcases: dict = cpast_llm.cpast_lib.generate(  # pyright: ignore[reportAttributeAccessIssue]
        clex
    )

    return CModels.LLMResponse(
        clex_lang=clex,
        generated_response=CModels.CpastLibResponse(
            Ok=generated_testcases.get('Ok'), Err=generated_testcases.get('Err')
        ),
    )


@app.get('/api/testcases/codeforces/{contest_id}/{problem_code}')
async def generate_testcase_codeforces(
    contest_id: str, problem_code: str
) -> CModels.LLMResponse:
    scrape_response: cpast_llm.cpast_utils.scrape_models.ScrapeAPIResponse = (
        codeforces.CodeForces().get_problems_by_code(contest_id, problem_code)
    )
    clex: str = generate_response(
        scrape_response.input_format,
        scrape_response.constraints,
        'codeforces',
        '{}/{}'.format(contest_id, problem_code),
    )

    generated_testcases: dict = cpast_llm.cpast_lib.generate(  # pyright: ignore[reportAttributeAccessIssue]
        clex
    )

    return CModels.LLMResponse(
        clex_lang=clex,
        generated_response=CModels.CpastLibResponse(
            Ok=generated_testcases.get('Ok'), Err=generated_testcases.get('Err')
        ),
    )


def generate_response(
    input_format: str,
    constraints: str,
    platform: Union[str, None] = None,
    question_identifier: Union[str, None] = None,
) -> str:
    if platform and question_identifier:
        cached_clex = clex_cache.retrieve_cache(platform, question_identifier)
        if cached_clex:
            return cached_clex

    chat_model = chat.ClexChatModel(
        GOOGLE_API_KEY, cpast_llm.cpast_utils.models.LANGCHAIN_LLM_CACHE_FILENAME
    )
    prompt_content = prompt.ClexPromptGenerator()
    lang_specs = prompt_content.get_lang_specs(path='./clex.spec.md')

    formatted_prompt_input = {
        'input_format': input_format,
        'constraints': constraints,
        'lang_specs': lang_specs,
    }

    clex = chat_model.call_model(
        prompt_content.get_dynamic_prompt(), input=formatted_prompt_input
    )
    if platform and question_identifier:
        clex_cache.add_cache(platform, question_identifier, clex)

    return clex
