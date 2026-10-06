from ollama import chat,ChatResponse
from ollama import Client
import os
from dotenv import load_dotenv


#############################################################

## preppeing the hostclient for VLA qwen3-v;:2b running on remotekaggle server.

load_dotenv('.env') # load the env variables from the .env folder.

# set up the url.
tunnel_url = os.getenv('NGROK_TUNNEL_PUBLIC_URL')

# Setup an Ollama client with the public ngrok host
client = Client(host=tunnel_url)

# pull and Pre-load the model on the server
client.pull(model="qwen3-vl:2b")

#######################################################################################################################

# create a simple chat request

'''resp : ChatResponse = chat(
    model="qwen3:1.7b",
    messages=[
        {
            'role':"user",'content':"hey tell me a 5 line story about the moon and the witch."
        }
    ],
    stream=False,
    think=False
)

#print(resp.message.content)'''

####################################################################################################
## now let's stream the responses.
'''streaming = chat(
    model="qwen3:1.7b",
    messages=[{
        'role':'user',
        'content':'tell me about the story of naruto and the lost sharingan! in about 3-4 lines.'
    }],
    stream=True,
    think=False
)

#for chunk in streaming:
#    print(chunk.message.content,end='',flush=True)'''

####################################################################################################

# Creating a conversation with chat history with local ollama model.

#####################################################################################################
yes = True
y=yes

models = {'text':'qwen3:1.7b','VLM':'qwen3-vl:2b'}

# now let's set the postgres knowledge base prompt.
knowledge = open("./sys_prompts/skill.txt","r",encoding="utf-8")

chat_history:list[dict] = [{'role':"system",
                            'content':knowledge.read()}]

knowledge.close()

# chat with VLM models.
def chatting_VLM(chat_history:list[dict],modeling:str):
    try:
        Stream_resp = client.chat(
            model=modeling,
            messages = chat_history,
            stream=True,
            think=False
        )
       
        # get the response.
        response_text = []

        for chunk in Stream_resp:
            response_text.append(chunk.message.content)
            print(chunk.message.content,end='',flush=True)

        # now append the response to the chat history as assistant message
        resp_string = " ".join(response_text)
        assistant_msg(resp_string)
        

    except Exception as e:
        print(f"error{e}")

## chatting with text models [ollama serve on localhost:11434 port], i.e our qwen3:1.7b
def chatting_text_model(chat_history:list[dict],modello:str):
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
            response_text.append(chunk.message.content)
            print(chunk.message.content,end='',flush=True)

        # now append the response to the chat history as assistant message
        resp_string = " ".join(response_text)
        assistant_msg(resp_string)


    except Exception as e:
        print(f"error occured: {e}")


'''# step 1. preparing the system message [fixed]
setContext1 = "you are storyteller witch from the 1500s from japan, you execl in telling horrific stories as 4-5 line poems"
setContext2 = "you are my freind and a helpful assistant"
def sys_msg(msg:str):
    sysMsg = {'role':"system",'content':msg}
    chat_history.append(sysMsg)'''


#step 2. preparing the user message [without attachments].
def user_msg(msg:str):
    userMsg = {'role':"user","content":msg}
    chat_history.append(userMsg)

# step 3. get the AI response message.
def assistant_msg(msg:str):
    assMsg = {'role':"assistant","content":msg}
    chat_history.append(assMsg)

## step 4: create a user prompt [with attachments].
def prompt_wit_att(msg:str,imgs:list[str]):
    att_prompt_field = {'images':imgs,'role':"user",'content':msg}
    chat_history.append(att_prompt_field)

## INITIALIZING THE CONVERSATION LOOP.

'''print("you can stop the conversation anytime by writng '/bye' ")
print(f" if you wanna include any attachment(s) just add '-a' to the message end after a space")

while y:
    # set the system message
    sys_msg(setContext2)
    
    n = input(">>> ")

    if len(n) == 0:
        pass

    elif n == "/bye":
        y = False

    else:
        if '-a' in n:
            # set the model to VLM i.e our qwen3-vl:2b paraketrs
            modeling = models['VLM']

            #get the user content/query first
            n_params = n.split("-a")

            # now ask for attachment(s) links.
            attachs = [str(i) for i in input("enter the attachemnt link/s [if multiple images, add a " " in b/w]").split(" ")]

            # set the prompt ad add it to chat_history.
            prompt_wit_att(n_params[0],attachs)

            # call the chat function to generate and stream the response.
            chatting_VLM(chat_history,modeling)

            
        else:
            # fall back to the by default text model i.e our qwen3:1.7b.
            modeling = models['text']

            # set the user messqage.
            user_msg(n)

            # # call the chat function to generate and stream the response.
            chatting_text_model(chat_history,modeling)


    print()
'''













