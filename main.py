from fastapi import FastAPI,Request, Response
from fastapi.responses import JSONResponse
from BodyRequest import *
from langchain import OpenAI, ConversationChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

app = FastAPI()
session_state = {}

OPENAI_API_KEY = "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"

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

    return Conversation.run(input=items.message)




