import google.generativeai as genai #type: ignore
import os
from dotenv import load_dotenv #type: ignore

load_dotenv()

# google_api_key = os.getenv("GOOGLE_API_KEY")
# print(f'google_api_key: f{google_api_key}')

class Genprompt:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)  # type: ignore
        self.model = genai.GenerativeModel("gemini-1.5-flash")  # type: ignore

    def generate_questions(self, input_text: str):
        """Generates 10 related questions and answers using Gemini LLM."""
        try:
            instruction = """
            <instruction>
            You are a question generator designed for a video conferencing tool used by elderly people. 
            Given a keyword, generate exactly 10 short, relevant, and easy-to-understand questions along with simple answers.

            **Rules:**
            - Each question should be concise and numbered.
            - Provide a short and easy-to-understand answer for each question.
            - Ensure the answers are **fact-based, simple, and conversational**.
            - Format the response exactly like the example below.

            <Example>:
            1. When did the Russia-Ukraine war start?  
               The war started on February 24, 2022, when Russia invaded Ukraine.  

            2. What were the main reasons for the war?  
               The conflict arose due to political tensions, NATO expansion concerns, and territorial disputes over regions like Crimea and Donbas.  

            3. How has the war affected Ukraine?  
               Ukraine has suffered major destruction, loss of lives, and displacement of millions of people.  

            4. What has been the response of the international community?  
               Many countries imposed sanctions on Russia, provided aid to Ukraine, and supported diplomatic efforts to end the war.  
            </Example>
            
            **Now, generate questions and answers for this keyword:**  
            Keyword: {keyword}

            Retrieve context.  
            </instruction>
            """

            prompt = instruction.format(keyword=input_text)
            response = self.model.generate_content(prompt)

            if response.text:
                lines = [line.strip() for line in response.text.strip().split(
                    "\n") if line.strip()]

                questions, answers = [], []
                for i in range(0, len(lines), 2):
                    if i + 1 < len(lines):
                        q = lines[i].lstrip("1234567890. ").strip()
                        a = lines[i + 1].replace("**Answer:**", "").strip()
                        questions.append(q)
                        answers.append(a)

                return {"questions": questions, "answers": answers}

            else:
                return {"questions": [], "answers": []}

        except Exception as e:
            return {"error": f"Error: {str(e)}"}


# # Testing the output
# if __name__ == "__main__":
#     gemini = Genprompt(google_api_key)
#     response = gemini.generate_questions("Milan")
#     print(response)
