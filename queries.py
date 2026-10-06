from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

from llamacorn import chat_history

# load the conection string.
load_dotenv("./.env")

# get the value.
conn_string = os.getenv("SUPABASE_CONNECTION_URL")

engine = create_engine(str(conn_string),echo=True)

# connection object.
con = engine.connect()


def append_sys(chat_history:list[dict],sys_prompt = str):
    knowledge_prompt = {'role':'system','content':sys_prompt}
    # appen this to global chat history as system prompt.
    chat_history.append(knowledge_prompt)

# low let's make the instruction prompt with schema enclosed in it (dynamic).
def make_ins():

    ## get schema content.
    schemaFile =open("./sys_prompts/schema.txt","r")
    schema = schemaFile.read()

    ## let's get the Instruction prompt.
    skillFile = open("./sys_prompts/ins.txt","r")
    Instructions = skillFile.read()

    # now let's set the postgres knowledge base prompt.
    knowledge = open("./sys_prompts/skill.txt","r",encoding="utf-8")
    know = knowledge.read()

    et = 0
    for i in range(len(skillFile.readlines())):
        if '{$}' in skillFile.readlines()[i]:
            et = i
            print(et)
            break

    # now spit the content into 3 ,replace 2nd one with schema and join them back => write into ins file.
    bfore = '\n'.join(skillFile.readlines()[:et])

    after = '\n'.join(skillFile.readlines()[et+1::])
    print(bfore)
    print(after)

    get_prompt = '\n'.join([bfore,schema,after])
    skillFile.close()

    # write into ins.
    with open('./sys_prompts/ins.txt','w',encoding="utf-8") as h:
        h.write(get_prompt)
        print('done!')

make_ins()
    











