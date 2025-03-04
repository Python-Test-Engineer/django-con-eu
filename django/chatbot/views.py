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
system_message = "You are a helpful assistant for a shoe store. If a user asks a question please be as helpful as possible and use a courteous and professional manner. You are provided with the following facts to help you. Please be verbose and suggestive."

# We add our own supplementary facts, this is RAG in that we are AUGMENTING our GENERATION through the use of RETRIEVAL - in this case it is a list but this wouldbe obtained from DB queries etc...
FAQ = [
    "We only sell shoes.",
    "Our opening hours are Monday to Friday from 9am to 5pm.",
    "We are located at 123 Main Street, Brighton",
    "We specialise in red shoes but have all colours",
    "Our VAT rate is 20 percent and is applicable on all sales",
    "We only accept card payments",
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
