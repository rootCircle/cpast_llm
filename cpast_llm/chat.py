from langchain.globals import set_llm_cache
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.cache import SQLiteCache


class ClexChatModel:
    def __init__(self, google_api_key, database_path: str = "../.langchain.db"):
        set_llm_cache(SQLiteCache(database_path=database_path))

        # Initialise gemini-pro for now
        self.model = self.__initialise_model(google_api_key)

    def __initialise_model(self, google_api_key, model: str = "gemini-pro"):
        return ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

    def call_model(self, prompt, input={}) -> str:
        chain = prompt | self.model
        result = chain.invoke(input=input)
        return result.content

