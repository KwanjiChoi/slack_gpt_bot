import unzip_requirements
import logging
import os
import random
import openai
import boto3
from datetime import datetime
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from llama_index import load_index_from_storage, StorageContext, LLMPredictor, ServiceContext, PromptHelper
from langchain.chat_models import ChatOpenAI

openai.api_key = os.environ['OPENAI_API_KEY']

### Set up index file and loader from here
s3 = boto3.client("s3")
s3.download_file(os.environ["S3_BUCKER_NAME"], "storage/docstore.json", '/tmp/docstore.json')
s3.download_file(os.environ["S3_BUCKER_NAME"], "storage/index_store.json", '/tmp/index_store.json')
s3.download_file(os.environ["S3_BUCKER_NAME"], "storage/vector_store.json", '/tmp/vector_store.json')

service_context = ServiceContext.from_defaults(
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=256)),
    prompt_helper = PromptHelper(max_input_size=3000, num_output=256, max_chunk_overlap=1)
)

storage_context = StorageContext.from_defaults(persist_dir="/tmp")
index = load_index_from_storage(
    storage_context = storage_context,
    service_context = service_context
)

os.remove('/tmp/docstore.json')
os.remove('/tmp/index_store.json')
os.remove('/tmp/vector_store.json')

query_engine = index.as_query_engine(
    similarity_top_k=2
)
### Set up index file and loader to here

app = App(
    process_before_response=True,
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

def acknowledge(ack):
    # Acknowledge a request within 3 seconds, to prevent Slack from retrying the request.
    ack()


import time
# Arg name should be event when use event method
def reply(event, say):
    # Sleep 5 sec for lazy listeners
    time.sleep(5)

    question = event['text']
    # Get slack thread ID
    thread = event['ts']

    answer = str(query_engine.query(question))
    say(answer, thread_ts=thread)

# Run event when mention chatBot
app.event(event="app_mention")(
    ack=acknowledge, lazy=[reply]
    )

# Clear the default log handler, and set up a basic one; CloudWatch will add timestamps automatically.
SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

def handler(event, context):
    if event['headers'].get('X-Slack-Retry-Reason') == "http_timeout":
        return {'statusCode': 200 }

    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
