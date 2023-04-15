from fastapi import FastAPI,Request, Response
from fastapi.responses import JSONResponse
from BodyRequest import *
from langchain import OpenAI, ConversationChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

app = FastAPI()
session_state = {}
load_dotenv()

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

llm = OpenAI(
        temperature=0,
        openai_api_key=OPENAI_API_KEY
    )

Conversation = ConversationChain(
                    llm=llm,
                    verbose=True,
                    memory=ConversationBufferMemory()
                )



@app.get('/')
async def index(request: Request) -> Response:
    return JSONResponse(content={"msg":"Welcome to chat-bot API"}, status_code=200)


@app.post('/chat-bot')
async def chatBot(request: Request) -> Response:

    jsonIncoming = await request.json()
    items = ItemBodyRequest(** jsonIncoming)

    if items.session_id not in session_state:
        session_state[items.session_id] = ConversationBufferMemory()

    Conversation.memory = session_state[items.session_id]
    output = Conversation.run(input=items.message)

    return {'msg': output}




