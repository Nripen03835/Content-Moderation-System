from moderator.prompt_builder import build_prompt
from moderator.mock_llm import generate_response
from moderator.parser import format_output


def moderate_text(user_text):
    prompt = build_prompt(user_text)

    # Call Groq API for moderation
    llm_output = generate_response(prompt)

    structured_output = format_output(llm_output, user_text)

    return structured_output
