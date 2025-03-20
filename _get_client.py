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
    llm_choice = "openai"
    # llm_choice = "groq"
    if llm_choice == "groq":
        model = "llama-3.3-70b-versatile"
    else:
        model = "gpt-4o-mini"

    system_message = """
    You are an assistant that is great at telling jokes.
    """

    # Here is where we can do some prompt engineering - we are adding to the system message and creating our endpoint as it were.
    prompt_engineering = """
    A joke worthy of publishing is a joke that has a rating of 8.5/10 or above.

    If the joke is worthy of publishing also include next: PUBLISH otherwise next: RETRY

    # Example

    Here is an example of a joke worth of publishing:

    Supply the response in the following JSON format:

    {"setup": "The setup of the joke",
    "punchline": "The punchline of the joke",   
    "rating": "9.0",
    "next": "PUBLISH"}

    Remove all back ticks and other unnecessary characters and just print the JSON format and nothing else.

    Please ensure jokes are not repeated on retries.

    """

    # We add the prompt engineering to the system message
    system_message += prompt_engineering

    # We create our user prompt and will add all of these to the payload.
    user_prompt = "Tell a light-hearted joke for an audience of Pythonistas"

    client = get_llm_client(llm_choice)
    print(client)

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
    print(answer)
