try:
  import unzip_requirements
except ImportError:
  pass

import logging
import os
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
import openai
import time
import boto3
from llama_index import GPTVectorStoreIndex, download_loader

openai.api_key = os.environ['OPENAI_API_KEY']

app = App(
    process_before_response=True,
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)


def acknowledge(ack):
    # Acknowledge a request within 3 seconds, to prevent Slack from retrying the request.
    ack()
# Arg name should be event when use event method
def reply(event, say):

    # Sleep 3 sec for lazy listeners
    time.sleep(3)

    question = event['text']
    # Get slack thread ID
    thread = event['ts']

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "user", "content": question }
          ],
    )

    gpt_answer = response.choices[0]["message"]["content"].strip()
    say(gpt_answer, thread_ts=thread)


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

# Run event when mention chatBot
app.event(event="app_mention")(ack=acknowledge, lazy=[reply])

# Clear the default log handler, and set up a basic one; CloudWatch will add timestamps automatically.
SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)