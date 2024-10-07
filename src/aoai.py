import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from getpass import getpass
import env

endpoint = env.ENDPOINT_URL
deployment = env.DEPLOYMENT_NAME

auth_method = "key"

if auth_method == "key":
  ## API key based auth
  AOAI_API_KEY = env.AOAI_API_KEY
  if not AOAI_API_KEY:
    AOAI_API_KEY = getpass("AOAI API Key: ")
    os.environ['AOAI_API_KEY'] = AOAI_API_KEY
    
  client = AzureOpenAI(
      azure_endpoint=endpoint,
      api_key=AOAI_API_KEY,
      api_version="2024-05-01-preview",
  )
else:
  ## Bearer Token Auth
  ## Should run `az login` first with your own Azure account.
  token_provider = get_bearer_token_provider(
      DefaultAzureCredential(),
      "https://cognitiveservices.azure.com/.default")
        
  client = AzureOpenAI(
      azure_endpoint=endpoint,
      azure_ad_token_provider=token_provider,
      api_version="2024-05-01-preview",
  )

def call_llm_API(message_list, tool_list=None, tool_choice=None):
  response = client.chat.completions.create(
      model=deployment,
      messages=message_list,
      max_tokens=1000,
      temperature=0.7,
      top_p=0.95,
      tools=tool_list,
      tool_choice=tool_choice,
  )
  # response = completion.choices[0].message.content
  return response


