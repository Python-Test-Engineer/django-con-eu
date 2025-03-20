import os
import openai
import groq
from dotenv import load_dotenv
from openai import OpenAI


def get_llm_client(llm_choice):
    if llm_choice == "groq":
        client = openai.OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        return client
    elif llm_choice == "openai":
        load_dotenv()  # load environment variables from .env file
        openai.api_key = os.getenv(
            "OPENAI_API_KEY"
        )  # get API key from environment variables
        client = OpenAI()
        return client
    else:
        raise ValueError("Invalid LLM choice. Please choose 'groq' or 'openai'.")


if __name__ == "__main__":
    # Example usage:
    # llm_choice = "openai"
    llm_choice = "groq"
    if llm_choice == "groq":
        model = "llama-3.3-70b-versatile"
    else:
        model = "gpt-4o-mini"

    system_message = """
    You are an assistant that is great at telling jokes.
    """

    # We create our user prompt and will add all of these to the payload.
    user_prompt = "Give me a general joke with your rating."

    client = get_llm_client(llm_choice)
    print(f"Always an OpenAI Client:\n {client} - {type(client)}")
    print("")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt},
        ],
        temperature=1.0,
    )
    answer = response.choices[0].message.content.strip()
    print(f"LLM Choice: {llm_choice}")
    print(f"Model: {model}")
    print("\nRESPONSE")
    print(answer)
