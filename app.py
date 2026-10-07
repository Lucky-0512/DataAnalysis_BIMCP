from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse , StreamingResponse
from fastapi import File,UploadFile ,Form

from pydantic import BaseModel

from pathlib import Path

# importing functions from custom file.
import llamacorn
from llamacorn import user_msg,assistant_msg,prompt_wit_att

import asyncllama

from llamacorn import chat_history,models

# creating an app instance.
app = FastAPI()

## to use / talk to JS/css or any assets on the frontend, we need to mount the static directory in fastapi.
app.mount("/src",StaticFiles(directory="src"),name="src")

## creating a jinja templating object [to returen any htm pages with dynamic support]
Templates = Jinja2Templates(directory="templates")

## get page.
@app.get("/",response_class=HTMLResponse)
def getPage(request:Request):

    return Templates.TemplateResponse(request=request,name="index.html",status_code=200)


'''class getQuery(BaseModel):
    query :str= Form(...)
    attachments: UploadFile = File(...)   ## this is the standard syntax to catch the blob files from JS.'''

from typing import List

@app.post("/query/user")
async def resp_query(query:str = Form(...),
                    uploaded_file: List[UploadFile] | None = File(None))  :

    # rules of QUERY HANDLING [heylets be strict here loll]
    # 1. if query = empty and attachment = empty => do nothing.
    # 2. if query = empty and attachment != empty => warn user to tell/instrcut => do ntg
    # 3. if query != empty :
        # => check if any attachment => yes => call the qwen3-vl:2b
        # => if no attchemnt => call the qwen3:1.7b txt model.
    
    user_query = str(query)
    user_attachments = uploaded_file

    try:

        if (user_query == None or user_query == '') :
            return {"resp":"do ntg"}
  
        elif (user_query == None or user_query == '') and (user_attachments != None):
            return {"status":"Please tell me what you wanna do with attachemnt..or cancel the attachemnt(s).."}

        elif user_query != None or user_query != '':
                        
            if ( (user_attachments) !=  None  ):
               ## save the attachment file and get the saved local url => append it to the list[strings]
                Base_url = Path.cwd() / "attachments"

                '''import os

                # first flush the files in attachments folders..
                for filename in os.listdir(Base_url):   # list all content of dir
                    file_path= os.path.join(Base_url,filename)

                    if os.path.isfile(file_path):  # chck if it's file only and not a dir
                        os.remove(file_path) # delete that file'''
                    

                user_attList = []


####################### PEDNING ...UNRESOLVED .... PENDING ...UNRESOLVED => handle the file size limits.

                for file in user_attachments:
                    if file.filename == '':
                        continue

                    contents = await file.read()  ### it's an async operation

                    file_path = Base_url / f'{file.filename}'

                    # now write the contents into a new file.
                    with open(file_path,'wb') as temp:
                        temp.write(contents)    
                        print(f"recieved file: {file.filename}")

                    # append the file path to the local dir.
                    user_attList.append(file_path)
                    print("file saved successfully!")

                vlm_model = models["VLM"]
                
                ## add attahcent prompt to chat history.
                prompt_wit_att(user_query,user_attList)

                call = asyncllama.chatting_VLM(chat_history=chat_history,modeling=vlm_model)

                return StreamingResponse(content=call,media_type="text/plain")
               

            else:
                ## add the user query to chat hstory via user_message.
                user_msg(user_query)

                text_model = models['text']

                ## apparentyl the chat model can only take the chat hisoty elemt if it's strucuted is like {role, content only ig}
                ## let's reformat the elements with key image => role and contentonly making them text only..
                
                txt_only_msgs = []

                for i in chat_history:
                    if "images" in i.keys():
                        txt_only_msgs.append({'role':i['role'],
                                              'content':i['content']})
                    else:   
                        txt_only_msgs.append(i)
                        

                call = asyncllama.chatting_text_model(chat_history=txt_only_msgs,modello=text_model,user_query=user_query)
                
                return StreamingResponse(content=call,media_type="text/plain")
                

    except Exception as e:
        print(f'error {e}')
        return e




    







