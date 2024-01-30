from langchain.prompts import PromptTemplate


class ClexPromptGenerator:
    def __init__(self):
        pass

    def get_lang_specs(self, path) -> str:
        with open(path) as f:
            specs: str = f.read()
            return specs

    def get_langchainPrompt(self):
        prompt = PromptTemplate.from_template(ClexPromptGenerator.__get_base_prompt())
        return prompt

    def __get_base_prompt() -> str:
        return """You are an expert at MAKING PROMPTS FOR LLMs for certain tasks.
        You are assigned with making a prompt for generating a language, based on set of certain rules.
        The RULES MUST BE FOLLOWED AT ANY COST.

        1. If you're unclear about the specifcations, then you won't generate the prompt, but ask me list of questions you have doubt with.
        2. I will be providing you with the specifcations of the language at the bottom, along with semantic meaning of some metacharacters used in the language and examples, if something feels incomplete please let me know.
        3. The purpose of this prompt would be that user will give input format for a program in human language and with the help of the prompt we should be able to convert it to the current language given, based on specifications.
        4. NEVER VIOLATE GRAMMAR RULES OF THE language

        Here is the specifications of the language
        {lang_spec}
        """


