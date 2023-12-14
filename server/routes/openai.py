import openai
from fastapi import APIRouter, Request, FastAPI
import urllib.parse
import json

from server.config.api_key import (
  api_key
)

from server.utils.response import (
  ResponseModel
)

openai.api_key = api_key

app = FastAPI()
router = APIRouter()


@router.get('/')
def root():
    return ResponseModel('Hi guy', 'This is a public endpoint')


openai.api_key = "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"


# Function to generate a response using ChatGPT
def generate_chatgpt_response(query):
  response = openai.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{
      'role': 'user',
      'content': f'Please answer about this question `'
                 f'{query}` and describe more details according to latest information of FOOTYSTATS reports.'
    }],
    temperature=0
  )
  
  return response.choices[0].message.content



@router.post('/start-response')
async def start_response():
  # return ResponseModel('this is the start', "start response")
  query = 'Hello! From now, You have to reply about football leagues all over the world. You have to interpret all information of FOOTYSTATS reports. ' \
          'For example, If I want to analyze the Real Madrid - Barcelona match. I will need all the statistical data of these two teams, player data and everything that the FOOTYSTATS API can provide me.'
  response = generate_chatgpt_response(query)
  return ResponseModel(response, "start response")



@router.post('/get-response')
async def get_response(request: Request):
    question = await request.body()
    decoded_string = urllib.parse.unquote(question)

    parsed_data = json.loads(decoded_string)
    print(f"#######################  {parsed_data['msg']}")
    txt = generate_chatgpt_response(parsed_data['msg'])
    return ResponseModel(txt, "This is a response")
    
