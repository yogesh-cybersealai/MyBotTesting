from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import openai
from config import *
import os
from openai import AsyncAzureOpenAI


#OpenAi Information
openai_client = AsyncAzureOpenAI(
    azure_endpoint="https://openai-ezaix.openai.azure.com",
    api_version="2023-03-15-preview",
    api_key="e6d38a5baf7a4f41bf87243a321c52cc",
)

class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text

        try:
            # Call OpenAI API to get a concise and summarized response
            response = await openai_client.chat.completions.create(
                model="gpt-4-0125",
                messages=[
                    {"role": "system", "content": "You are an expert in Microsoft Teams. Provide detailed and concise answers to user queries related to Microsoft Teams. Where possible, reference information from learn.microsoft.com to enrich the user experience."},
                    {"role": "user", "content": f"{user_input}"}
                ],
                max_tokens=300,  # Adjusting max_tokens for faster responses
                temperature=0.5  # Lowering temperature for more focused responses            )
            )
            # Print the entire response for debugging
            # print(response)

            # Extract the text from the OpenAI response
            openai_response = response.choices[0].message.content.strip()

            # Send the response back to the user
            await turn_context.send_activity(openai_response)

        except openai.RateLimitError:
            await turn_context.send_activity("The bot has exceeded its usage limits for the moment. Please try again later.")
        except openai.APIConnectionError as e:
            print("The server could not be reached")
            await turn_context.send_activity(f"An error occurred: {e.__cause__}")
        except Exception as e:
            await turn_context.send_activity(f"An unexpected error occurred: {str(e)}")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
