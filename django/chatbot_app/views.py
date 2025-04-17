import os
from django.shortcuts import render
from .models import Message
import requests
from dotenv import load_dotenv, find_dotenv
from rich.console import Console

console = Console()
# Load in our API keys
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
console.print(f"[dark_orange]OPENAI_API_KEY: {OPENAI_API_KEY[:14]}...[/]")


# We add in our own system message
system_message = "You are a helpful assistant for a shoe store. If a user asks a question please be as helpful as possible and use a courteous and professional manner. You are provided with the following facts to help you. Please be CONCISE but SUGGESTIVE."

# We add our own supplementary facts, this is RAG in that we are AUGMENTING our GENERATION through the use of RETRIEVAL - in this case it is a list but this wouldbe obtained from DB queries etc...
FAQ = [
    "DjangoCon 2025 is taking place in Dublin",
    "The dates are 23rd-27th April 2025",
    "The venue is DjangoCon Europe 2025 will be held in Dublin! The capital of the Republic of Ireland, one of Europe’s biggest tech hubs, is a lively city with extraordinarily rich and diverse food, culture, history and art lovers - the number of museums and restaurants can certainly tickle most tastes.",
    "The conference will take place at Talbot Hotel Stillorgan, Dublin",
    "As an EU/EEA resident, you do not require a visa to travel to Ireland. You can enter the country freely under the Common Travel Area (CTA) agreements.",
    """
    Documents to Carry
    Even though a visa is not required, ensure you carry:
    - A valid passport or national ID card.
    - Proof of accommodation (e.g., hotel bookings or host details).
    - Your DjangoCon Europe ticket or event confirmation.
    - Travel insurance (optional but recommended).
    """,
    "DjangoCon Europe 2025 offers grants so that those who might otherwise not be able to attend won't hesitate to participate. Some expenses for the conference attendance (which could include travel, hotel, registration, etc) will be covered for opportunity grant recipients.",
    "The sponsors are Ambient, Caktus, Monit to name but a few.",
    """
    Mentorship Program
    Are you an experienced speaker eager to share your knowledge and guide aspiring speakers? Or are you planning to submit a proposal to DjangoCon Europe 2025 and looking for expert advice to craft a standout submission?
    If you answered 'yes' to either question, this mentorship program is perfect for you!
    """,
    """ 
    For Mentees This is How the Program Works
    Our aim is to pair each mentee with a dedicated mentor to foster one-on-one guidance. To simplify scheduling, we prioritize matching participants in the same timezone or country whenever possible.
    """,
    """
    A live recording of a 'The Real Python Podcast' episode with audience participation.

    The Real Python Podcast is a weekly podcast hosted by Christopher Bailey with interviews, coding tips, and conversations with guests from the Python community. Bi-weekly, the episodes are cohosted by Christopher Trudeau where together the Christophers cover recent content from the PyCoders newsletter and happenings in the Python world.

    The DjangoCon session would be similar to PyCoders episodes where we cover interesting recent Python articles. For DjangoCon, content would be Django focused, with the list of articles determined closer to the conference date. Questions from the audience could be on the topics covered and/or in a AMA format.""",
    """Sprints
So you have listened to all the exciting topics on django for three days and now feel motivated do something about it. What could be a better motivation than contributing to the very open source software you just listened to?

On Saturday and Sunday, you have the opportunity to do exactly that. This is your opportunity to contribute to Open Source software. Even if you haven't contributed before, this is also an option to take your first steps. In the sprint, you can contribute to Django as you see fit, and if you need help, there will a pool of experienced contributors to guide you.

Main Venue - Hosting our Sprints
Talbot Hotel Stillorgan

Time
Saturday - 9AM to 6PM
Sunday - 9AM to 6PM
The Sprints are free for all conference participants. However, as the Sprints venue does not have unlimited capacity, and we would like to prepare a precise amount of food and drinks, please keep your participation status updated on the ticketing website (after buying your ticket).

We will be hosting our sprints at Talbot Hotel Stillorgan. Get ready for an amazing conference experience in beautiful Dublin!

Check the map to the venue""",
]

# Create the base system message
system_message += "\n" + "\n".join(FAQ)


def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        bot_message = get_ai_response(user_message)
        Message.objects.create(user_message=user_message, bot_message=bot_message)
    messages = Message.objects.all()
    return render(request, "chat.html", {"messages": messages})


def get_ai_response(user_input: str) -> str:
    # Set up the API endpoint and headers for LLM query
    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    # Data payload - We get all existing messages from the database
    messages = get_existing_messages()
    messages.append(
        {"role": "user", "content": f"{user_input}"},
    )
    messages.append(
        {"role": "system", "content": system_message},
    )
    data = {"model": "gpt-3.5-turbo", "messages": messages, "temperature": 0.7}
    # Here is our LLM query
    response = requests.post(endpoint, headers=headers, json=data)
    response_data = response.json()
    print(f"{response_data = }")
    # We can extract the response
    ai_message = response_data["choices"][0]["message"]["content"]
    return ai_message


def get_existing_messages() -> list:
    """
    Get all messages from the database and format them for the API in terms of user and assistant messages.
    """
    formatted_messages = []

    for message in Message.objects.values("user_message", "bot_message"):
        formatted_messages.append({"role": "user", "content": message["user_message"]})
        formatted_messages.append(
            {"role": "assistant", "content": message["bot_message"]}
        )

    return formatted_messages
