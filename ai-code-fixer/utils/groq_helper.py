import os
import json
import re

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv('GROQ_API_KEY')
)

MODEL = 'llama-3.1-8b-instant'


# ==========================================
# AI CODE ANALYSIS + FIXING
# ==========================================

def analyze_and_fix(
    code,
    issues,
    language='python'
):

    prompt = f"""
You are an expert {language} debugger and software engineer.

Your task:
- Fix the provided code
- Explain issues simply
- Suggest improvements
- Keep original logic intact

IMPORTANT:
- Return ONLY valid JSON
- No markdown
- No extra text
- No ```json

Code:
{code}

Issues:
{chr(10).join(issues)}

Return EXACTLY this format:

{{
    "explanation": "short explanation",
    "fixed_code": "corrected code",
    "improvements": [
        "improvement 1",
        "improvement 2"
    ]
}}
"""

    try:

        chat_completion = (
            client.chat.completions.create(

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                model=MODEL,

                temperature=0.1
            )
        )

        response = (
            chat_completion
            .choices[0]
            .message.content
            .strip()
        )

        return parse_groq_response(
            response,
            code
        )

    except Exception as e:

        return {

            "explanation":
            f"Groq API Error: {str(e)}",

            "fixed_code":
            code,

            "improvements": [
                "Check internet connection",
                "Check Groq API key"
            ]
        }


# ==========================================
# PARSE AI JSON RESPONSE
# ==========================================

def parse_groq_response(
    response,
    original_code
):

    try:

        # remove markdown
        response = re.sub(
            r'```json',
            '',
            response
        )

        response = re.sub(
            r'```',
            '',
            response
        )

        response = response.strip()

        # extract JSON safely
        json_start = response.find('{')

        json_end = (
            response.rfind('}')
            + 1
        )

        if (
            json_start == -1 or
            json_end == 0
        ):

            raise ValueError(
                "No valid JSON found"
            )

        json_str = response[
            json_start:json_end
        ]

        data = json.loads(json_str)

        return {

            "explanation":

            data.get(
                "explanation",
                "No explanation available"
            ),

            "fixed_code":

            data.get(
                "fixed_code",
                original_code
            ),

            "improvements":

            data.get(
                "improvements",
                []
            )
        }

    except Exception as e:

        return {

            "explanation":
            f"Parsing failed: {str(e)}",

            "fixed_code":
            original_code,

            "improvements": [
                "AI response formatting issue"
            ]
        }


# ==========================================
# AI CHAT ASSISTANT
# ==========================================
def analyze_chat(message):

    prompt = f"""
You are NeuroFix AI.

You are an intelligent coding mentor and developer assistant.

Your goal is to explain concepts the way an excellent teacher would.

Response Style:
- Natural and human-like
- Educational but not textbook-like
- Clear and practical
- Easy to study from
- Beginner friendly
- Technical when needed

Rules:
- Do not use motivational phrases
- Do not say "don't worry", "great question", etc.
- Avoid long introductions
- Avoid unnecessary theory
- Give direct explanations
- Use examples only when useful
- Explain the WHY behind concepts
- Keep answers focused

Preferred Structure:

Concept:
(2-3 sentence explanation)

Example:
(if useful)

Why it matters:
(short practical explanation)

User Question:
{message}
"""

    try:

        chat_completion = (
            client.chat.completions.create(

                messages=[

                    {
                        "role": "system",
                        "content":
                        "You are a professional coding mentor."
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                model=MODEL,

                temperature=0.4,

                max_tokens=600
            )
        )

        response = (
            chat_completion
            .choices[0]
            .message.content
            .strip()
        )

        response = response.replace(
            "**",
            ""
        )

        return response

    except Exception as e:

        return (
            f"AI Chat Error: {str(e)}"
        )