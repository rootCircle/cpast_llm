from pydantic import BaseModel


class LLMRequest(BaseModel):
    real_input_format: str
    real_constraints: str

    model_config = {
        'json_schema_extra': {
            'example': {
                'real_input_format': 'First line will contain T, number of test cases. Then the test cases follow.\nThe first line of each test case contains two integers N and K.\nThe second line contains the string S.',
                'real_constraints': "1≤T≤1000\n1≤N≤10^6\n1≤K≤10^6\nS consists of 0 and 1 only.\nThe sum of N and K over all test cases won't exceed 5⋅10^6.",
            }
        }
    }


class CpastLibResponse(BaseModel):
    Ok: str | None = None
    Err: str | None = None


class LLMResponse(BaseModel):
    clex_lang: str
    generated_response: CpastLibResponse


class TestcaseRequest(BaseModel):
    clex: str
    iterations: int

    model_config = {
        'json_schema_extra': {
            'example': {'clex': "(N[1,10]) (?:S[3,'U']){\\1}", 'iterations': 5}
        }
    }


class TestcaseResponse(BaseModel):
    testcases: list[CpastLibResponse]


class LLMGenerateResponse(BaseModel):
    clex: str
