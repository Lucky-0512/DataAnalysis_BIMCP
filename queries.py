from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# load the conection string.
load_dotenv("./.env")

# get the value.
conn_string = os.getenv("SUPABASE_CONNECTION_URL")

engine = create_engine(str(conn_string),echo=True)

# connection object.
con = engine.connect()


def append_ins(chat_history:list[dict]):
    
    # low let's make the instruction prompt with schema enclosed in it (dynamic).
    def make_ins():

        ## get schema content.
        schemaFile =open("./sys_prompts/schema.txt","r")
        schema = schemaFile.read()

        ## let's get the Instruction prompt.
        skillFile = open("./sys_prompts/ins.txt","r")

        et = 0
        for i,val in enumerate(skillFile.readlines()):
            if "{$}" in val:
                et = i
                break

        # now spit the content into 3 ,replace 2nd one with schema and join them back => write into ins file.
        
        # reset the file pointer
        skillFile.seek(0)
        bfore = ''.join(skillFile.readlines()[:et])

        # reset the file pointer 2nd time
        skillFile.seek(0)
        after = ''.join(skillFile.readlines()[et+1::])
    
        get_prompt = ''.join([bfore,schema,after])

        with open("./pmp.txt",'w') as gg:
            gg.write(get_prompt)

        skillFile.close()
        schemaFile.close()
        gg.close()

    make_ins() ## make of the instruction prompt successfult saved to => pmp.txt

    read_ins_prompt = open("./sys_prompts/pmp.txt",'r').read() # read the written content

    ins_prompt = {'role':'system','content':read_ins_prompt} # prep the dict element.
    
    chat_history.append(ins_prompt) # appen to global chat history as system prompt.













