from ollama import Client
from ollama import chat

import os
from dotenv import load_dotenv

from llamacorn import user_msg,assistant_msg,prompt_wit_att

from queries import querying_agent

#############################################################

def configure_vlm():
    ## preppeing the hostclient for VLA qwen3-v;:2b running on remotekaggle server.

    load_dotenv('.env') # load the env variables from the .env folder.

    # set up the url.
    tunnel_url = os.getenv('NGROK_TUNNEL_PUBLIC_URL')

    # Setup an Ollama client with the public ngrok host
    cloud_client = Client(host=tunnel_url)


    cloud_client.pull(model="qwen3-vl:2b")

    return cloud_client

cloud_cli = configure_vlm()

# chat with VLM models.
def chatting_VLM(chat_history:list[dict],modeling:str):

    try:
        Stream_resp = cloud_cli.chat(
            model=modeling,
            messages = chat_history,
            stream=True,
            think=False
        )
       
        # get the response.
        response_text = []

        for chunk in Stream_resp:
            if chunk and chunk.message and chunk.message.content:
                response_text.append(chunk.message.content)
                yield chunk.message.content
        
        # now append the response to the chat history as assistant message
        resp_string = "".join(response_text)
        assistant_msg(resp_string)

    except Exception as e:
        print(f"error{e}")
        yield f'erroe{e}'


## chatting with text models [ollama serve on localhost:11434 port], i.e our qwen3:1.7b
def chatting_text_model(chat_history:list[dict],modello:str,user_query:str):
    try:
        Stream_resp = chat(
            model=modello,
            messages=chat_history,
            stream=True,
            think=False,
        )
               
        # get the response.
        response_text = []

        for chunk in Stream_resp:
            if chunk and chunk.message and chunk.message.content:
                response_text.append(str(chunk.message.content))
                yield chunk.message.content

        # now append the response to the chat history as assistant message
        resp_string = "".join(response_text)
        assistant_msg(resp_string)

        print("RAW MODEL RESPONSE:", (resp_string))

        # convert response string to json.
        import json
        json_resp = json.loads(resp_string)

        if json_resp["db_required"]:
            ## send the query to nlp2sql model => call the model here..
            result_query = querying_agent(query=user_query)
            if result_query:
                print("analysing....")
                # call the resp object again, feed this as input to chat model, and then append the resp to global chat history.
                res_result = chat(
                    model="qwen3:1.7b",
                    messages=[{'role':"user","content":user_query},{'role':"assistant","content":result_query}],
                    stream=True,
                    think=False
                )

                # get the response.
                resp_analysis = []

                for chunk in res_result:
                    if chunk and chunk.message and chunk.message.content:
                        resp_analysis.append(chunk.message.content)
                        yield chunk.message.content
                ## append this as string to global chat_history.
                analysis_str = ''.join(resp_analysis)
                assistant_msg(msg=analysis_str)


    except Exception as e:
        print(f"error occured: {e}")
        yield f'error{e}'



