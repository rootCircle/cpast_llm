from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    PromptTemplate,
)


class ClexPromptGenerator:
    def __init__(self):
        pass

    def get_lang_specs(self, path) -> str:
        with open(path) as f:
            specs: str = f.read()
            return specs

    def get_dynamic_prompt(self):
        example_prompt = PromptTemplate(
            input_variables=['input_format', 'constraints', 'generated_language'],
            template=self.__get_prompt_template(),
        )

        example_prompt = ChatPromptTemplate.from_messages(
            [
                ('human', 'Input Format : {input_format}\nConstraints : {constraints}'),
                ('ai', '{generated_language}'),
            ]
        )

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=self.__get_examples(),
        )

        final_prompt = ChatPromptTemplate.from_messages(
            [
                ('system', self.__get_prompt_template()),
                few_shot_prompt,
                (
                    'human',
                    'Input Format : {real_input_format}\nConstraints : {real_constraints}',
                ),
            ]
        )

        return final_prompt

    def __get_examples(self) -> list:
        # Examples of a pretend task of creating antonyms.
        return [
            {
                'input_format': 'The first line contains an integer T, the number of test cases. Then T test cases follow. Each test case contains an integer p. ',
                'constraints': ' 1 ≤ T ≤ 5\n1 ≤ p ≤ 100000 (105)\nThere exists combinations of menus whose total price is exactly p.',
                'generated_language': '(N[1,5]) (?:N[1,100000]){\\1}',
            },
            {
                'input_format': 'The first line of input will contain a single integer T, denoting the number of test cases.\nEach test case consists of two space-separated integers N and M — the number of students wants to go and the total number of tickets available, respectively.',
                'constraints': '1≤T≤1000\n1≤N,M≤10^5',
                'generated_language': '(N[1,1000]) (?:N[1,100000] N[1,100000]){\\1}',
            },
        ]

    def __get_prompt_template(self) -> str:
        return """You are an expert at MAKING PROMPTS FOR LLMs for certain tasks.
        You are assigned with making a prompt for generating a language, based on set of certain rules.
        The RULES MUST BE FOLLOWED AT ANY COST.

        1. If you're unclear about the specifications, then you WON'T GENERATE the prompt, but you will ask me list of questions you have doubt with.
        2. I will be providing you with the specifications of the language at the bottom, along with semantic meaning of some metacharacters used in the language and examples, if something feels incomplete please let me know.
        3. The purpose of this prompt would be that user will give input format for a program in human language and with the help of the prompt we should be able to convert it to the current language given, based on specifications.
        4. NEVER VIOLATE GRAMMAR RULES OF THE language

        Here is the specifications of the language
        {lang_specs}
        """
