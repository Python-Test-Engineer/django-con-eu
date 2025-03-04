# Django ChatGPT Chatbot

## OpenAI Key

*Ensure you login first with admin/password in admin site.*

admin and password

Then go to [site](http://127.0.0.1:8000/).

This works with OpenAI Key saved in the .env file.

Rename `.env.sample` to `.env` and supply your OpenAI Key.

Usual Django set up - this works with `python manage.py runserver` with admin/password as credentials.

Go to site/admin and login then got to site/chatbot or site/chatbot_app.

The app 'chatbot' with views.py is the example we used of FAQ.

Another chatbot `chatbot_app` uses HTMX rather than JS - Thanks to Tom Dekan for this and can be found on YouTube [https://www.youtube.com/watch?v=Y8GjRrotz6M](https://www.youtube.com/watch?v=Y8GjRrotz6M)

[http://127.0.0.1:8000/chatbot-app/](http://127.0.0.1:8000/chatbot-app/) to see this app