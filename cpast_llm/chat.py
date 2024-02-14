from langchain.globals import set_llm_cache
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.cache import SQLiteCache
from langchain_core.pydantic_v1 import SecretStr


class ClexChatModel:
    def __init__(
        self, google_api_key: SecretStr, database_path: str, model: str = 'gemini-pro'
    ):
        set_llm_cache(SQLiteCache(database_path=database_path))

        # Initialise gemini-pro for now
        self.model = self.__initialise_model(google_api_key, model)

    def __initialise_model(self, google_api_key: SecretStr | None, model: str):
        return ChatGoogleGenerativeAI(
            model='gemini-pro',
            google_api_key=google_api_key,
            convert_system_message_to_human=True,
            client=None,
            client_options=None,
            transport=None,
        )

    def call_model(self, prompt, input: dict | None = None) -> str:
        if input is None:
            input = {}
        chain = prompt | self.model
        result = chain.invoke(input=input)
        return result.content
