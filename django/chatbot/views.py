# The FAQ example from 03_faq.ipynb using either OpenAI or Groq.
# Refactoring so that can have the LLM choice as a config variable has not been done.

# SYSTEM
import os

# DJANGO
from django.contrib import auth
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Chat

# LLM
from openai import OpenAI
import openai

# OTHER
from dotenv import load_dotenv, find_dotenv
from rich.console import Console

console = Console()

# Load in our API keys
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
console.print(f"[dark_orange]OPENAI_API_KEY: {OPENAI_API_KEY[:14]}...[/]")
print()
console.print(f"[cyan]GROQ_API_KEY: {GROQ_API_KEY[:14]}...[/cyan]")

# We add in our own system message
system_message = """You are a helpful assistant for the Django Conference. Be brief but complete."""

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
]


# Create the base system message
system_message += "\n" + "\n".join(FAQ)


# Helper function for OpenAI calls
def ask_openai(message):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": message},
        ],
    )
    answer = response.choices[0].message.content.strip()
    return answer


# Helper function for GROQ calls
def ask_groq(message):
    # GROQ
    client = openai.OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_API_KEY,
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ],
    )
    answer = response.choices[0].message.content.strip()
    return answer


# Here is the Chatbot
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == "POST":
        message = request.POST.get("message")
        # REFACTORING better so that we can set choice of LLM once in a config file but not done for this demo.
        response = ask_openai(message)
        # response = ask_groq(message)

        chat = Chat(
            user=request.user,
            message=message,
            response=response,
            created_at=timezone.now,
        )
        chat.save()
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html", {"chats": chats})


# This uses a different template with a ChatGPT look.
def chatbot_groq(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == "POST":
        message = request.POST.get("message")
        response = ask_groq(message)

        chat = Chat(
            user=request.user,
            message=message,
            response=response,
            created_at=timezone.now,
        )
        chat.save()
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot_groq.html", {"chats": chats})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("chatbot")
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error_message": error_message})
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect("chatbot")
            except:
                error_message = "Error creating account"
            return render(request, "register.html", {"error_message": error_message})
        else:
            error_message = "Password don't match"
            return render(request, "register.html", {"error_message": error_message})
    return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect("login")


# Test
def index(request):
    return render(request, "home.html")
