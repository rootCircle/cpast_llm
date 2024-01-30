
import cpast_llm.prompt as prompt
import cpast_llm.chat as chat

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# chat_prompt = ChatGoogleGenerativeAI()


def main():
    chat_model = chat.ClexChatModel(GOOGLE_API_KEY)
    prompt_content = prompt.ClexPromptGenerator()
    lang_specs = {"lang_spec": prompt_content.get_lang_specs(path="./clex.spec.md")}
    print(chat_model.call_model(prompt_content.get_langchainPrompt(), input=lang_specs))


if __name__ == "__main__":
    main()
