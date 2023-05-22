import os
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

app = App(
    process_before_response=True,
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

# Run event when mention chatBot
@app.event("app_mention")
# Arg name should be event when use event method
def reply(event, say):

    print(event)

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

def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)