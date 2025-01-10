#%%
import chainlit as cl
import requests
import json
from chatbot import question_router, create_event

# On chat start, welcome message
@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome! How can I assist you today?").send()

# On receiving a message
@cl.on_message
async def on_message(message: cl.Message):
    try:
        # Make the POST request
        json_response = requests.post(
            "http://localhost:8080/invoke",
            json={
                "input": {
                    "question": message.content,
                    "generation": "string",
                    "web_search": "string",
                    "documents": ["string"],
                },
                "config": {
                    "configurable": {
                        "thread_id": 12,
                        "thread_ts": "string",
                    }
                },
                "kwargs": {},
            },
        )

        # Check for successful response status
        json_response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

        # Attempt to parse JSON from the response, if valid
        try:
            json_data = json_response.json()
        except json.JSONDecodeError:
            cl.logger.error(f"JSONDecodeError: Could not decode JSON from the response. Raw response: {json_response.text}")
            await cl.Message(content="Sorry, I received an invalid response from the server.").send()
            return

        # Extract response data
        if 'output' in json_data and 'generation' in json_data['output']:
            response = json_data['output']['generation']
        else:
             cl.logger.error(f"JSONDecodeError: Could not extract generation from the JSON. JSON: {json_data}")
             await cl.Message(content="Sorry, I could not process the response.").send()
             return

        # Assuming 'question_router' is already defined and imports handled
        datasource = question_router.invoke({"question": message.content})
        datasource = datasource['datasource']

        if datasource == "booking":
            await cl.Message(content="Please provide the following details to book a meeting:").send()
            await cl.Input(id="client_email", label="Client's Email", type="text").send()
            await cl.Input(id="meeting_date", label="Meeting Date (YYYY-MM-DD)", type="text").send()
            await cl.Input(id="meeting_time", label="Meeting Time (HH:MM)", type="text").send()
            await cl.Button(id="book_meeting", label="Book Meeting", on_click=book_meeting).send()
        else:
            await cl.Message(content=response).send()

    except requests.exceptions.RequestException as e:
        cl.logger.error(f"RequestException: An error occurred during the request to http://localhost:8080/invoke: {e}")
        await cl.Message(content="Sorry, there was a problem communicating with the server.").send()
        return


# Booking meeting function
async def book_meeting():
    client_email = await cl.get_input("client_email")
    meeting_date = await cl.get_input("meeting_date")
    meeting_time = await cl.get_input("meeting_time")
    
    # Event creation logic
    start_time = f"{meeting_date}T{meeting_time}:00Z"
    
    response = create_event("doctor@example.com", client_email, "Client Name", start_time)
    await cl.Message(content=response).send()
#%%