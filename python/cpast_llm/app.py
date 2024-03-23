import cpast_prompt.prompt as prompt
import cpast_prompt.chat as chat
import cpast_scrapper.codeforces as codeforces
import cpast_scrapper.codechef as codechef
import cpast_scrapper.constant
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.pydantic_v1 import SecretStr
import cpast_utils.env_util
import cpast_utils.models as CModels
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


@app.post('/api/llm/generate')
async def llm_generate(request: CModels.LLMRequest) -> CModels.LLMResponse:
    clex: str = generate_response(request.real_input_format, request.real_constraints)

    generated_testcases: dict = cpast_lib.generate(  # pyright: ignore[reportAttributeAccessIssue]
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
        clex=generate_response(request.real_input_format, request.real_constraints)
    )


@app.post('/api/testcases/generate')
async def testcase_generate(
    request: CModels.TestcaseRequest,
) -> CModels.TestcaseResponse:
    testcases: CModels.TestcaseResponse = CModels.TestcaseResponse(testcases=[])
    for _ in range(request.iterations):
        generated_testcases: dict = cpast_lib.generate(  # pyright: ignore[reportAttributeAccessIssue]
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
) -> cpast_scrapper.constant.ScrapeAPIResponse:
    return codechef.CodeChef().get_problems_by_code(problem_code)


@app.get('/api/code/codeforces/{contest_id}/{problem_code}')
async def get_codeforces_problem(
    contest_id: str, problem_code: str
) -> cpast_scrapper.constant.ScrapeAPIResponse:
    return codeforces.CodeForces().get_problems_by_code(contest_id, problem_code)


def generate_response(real_input_format: str, real_constraints: str) -> str:
    chat_model = chat.ClexChatModel(GOOGLE_API_KEY, './.langchain.db')
    prompt_content = prompt.ClexPromptGenerator()
    lang_specs = prompt_content.get_lang_specs(path='./clex.spec.md')

    formatted_prompt_input = {
        'real_input_format': real_input_format,
        'real_constraints': real_constraints,
        'lang_specs': lang_specs,
    }

    response = chat_model.call_model(
        prompt_content.get_dynamic_prompt(), input=formatted_prompt_input
    )

    return response
