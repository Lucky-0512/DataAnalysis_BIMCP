from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from pydantic import BaseModel


# importing functions from custom file.
from llamacorn import user_msg,assistant_msg,prompt_wit_att

from llamacorn import chatting_text_model , chatting_VLM

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


class getQuery(BaseModel):
    query : str | None
    attachments: list[str]

@app.post("/query/user")
async def resp_query(data:getQuery):

    # rules of QUERY HANDLING [heylets be strict here loll]
    # 1. if query = empty and attachment = empty => do nothing.
    # 2. if query = empty and attachment != empty => warn user to tell/instrcut => do ntg
    # 3. if query != empty :
        # => check if any attachment => yes => call the qwen3-vl:2b
        # => if no attchemnt => call the qwen3:1.7b txt model.
    
    user_query = data.query
    user_attachments = data.attachments

    try:

        if (user_query == None or user_query == '') :
            return {"resp":"do ntg"}

        elif (user_query == None or user_query == '') and (len(user_attachments) == 0):
            return {"status":"Please tell me what you wanna do with attachemnt..or cancel the attachemnt(s).."}

        elif user_query != None or user_query != '':

            ## add the user query to chat hstory via user_message.
            user_msg(user_query)
            
            if (len(user_attachments)!=0):
                vlm_model = models["VLM"]
                chatting_VLM(chat_history=chat_history,modeling=vlm_model)



                ### noooooo, im doing smthig worn here,, coz all the functions from llamacorn .p works on synchrounnous client..
                # but we need apply them on async Client. it's better to create anopther file , copy paste asame fucntion , with Async client,
                # and modify the rturn behavior to suit the asynchronous behavor that can work on frontend too.



    except Exception as e:
        print(f'error {e}')
        return e




    







