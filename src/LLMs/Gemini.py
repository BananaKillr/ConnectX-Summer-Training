from langchain_google_genai import ChatGoogleGenerativeAI
from Config.config import get_settings
from langchain_core.prompts import ChatPromptTemplate
from Prompts.prompts import LLMPrompts

class GEMINI:
    def __init__(self):
        self.settings = get_settings()
        self.llm = ChatGoogleGenerativeAI(google_api_key=self.settings.GOOGLE_API_KEY,
                                          model="gemini-2.5-flash")       

    def build_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    LLMPrompts.SYSTEM_PROMPT.value,
                ),
                ("human",LLMPrompts.HUMAN_PROMPT.value),
            ]
        )
    
    def run(self,user_question: str,retrieved_context: str):
        prompt_template = self.build_prompt()
        chain =  prompt_template | self.llm          
        return chain.invoke(
            {
                "context": retrieved_context,
                "question": user_question,
            }
        )





        
        

        

