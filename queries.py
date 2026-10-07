from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

from sqlalchemy import text
from ollama import chat

# load the conection string.
load_dotenv("./.env")

# get the value.
conn_string = os.getenv("SUPABASE_CONNECTION_URL")

engine = create_engine(str(conn_string),echo=True)

# connection object.
con = engine.connect()

knowledging = open("./sys_prompts_nlp2sql/skill.txt",'r',encoding="utf-8") # open the knowledge file

hist_nlp2sql = [{'role':"system","content":knowledging.read()}]  # a seperate chat history for the nlp2sql model.

knowledging.close() # close the knowlege prmpt file.

def append_ins(chat_history:list[dict]):
    
    # low let's make the instruction prompt with schema enclosed in it (dynamic).
    def make_ins():

        ## get schema content.
        schemaFile =open("./sys_prompts_nlp2sql/schema.txt","r")
        schema = schemaFile.read()

        ## let's get the Instruction prompt.
        skillFile = open("./sys_prompts_nlp2sql/ins.txt","r")

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

        with open("./sys_prompts_nlp2sql/pmp.txt",'w') as gg:
            gg.write(get_prompt)

        skillFile.close()
        schemaFile.close()
        gg.close()

    make_ins() ## make of the instruction prompt successfult saved to => pmp.txt

    read_ins_prompt = open("./sys_prompts_nlp2sql/pmp.txt",'r').read() # read the written content

    ins_prompt = {'role':'system','content':read_ins_prompt} # prep the dict element.
    
    chat_history.append(ins_prompt) # appen to global chat history as system prompt.

append_ins(hist_nlp2sql)

#############################################################################################

def querying_agent(query:str) -> str:
    global hist_nlp2sql
    # add th query to the history.
    hist_nlp2sql.append({'role':"user",'content':query})

    resp = chat(
        model= "qwen3:1.7b",
        messages=hist_nlp2sql,
        think=False
    )

    # parsing str to json.
    import json
    resp_json = json.loads(str(resp.message.content))

    ## now implement each query to the supabase postgres
    resp_queries = []
    for j in resp_json:
        resp_queries.append(j)

    # now query each query valueform every element in evry dict element to postres.

    # CREATING A RESPONSE QUERY.
    for query_el in resp_queries:
        if query_el.get("need") == "INSUFFICIENT_SCHEMA":
            query_el["result"] = None
            continue
            

        get_result = con.execute(text(query_el['query']))

        data = get_result.mappings().all()
        data = [dict(row) for row in data] 
        # this is the table that is reprsewnted as a list of dictioaries, where each dictionary = row.

        # now append this data element to the query el.
        query_el["result"] = data

    ## now convert the reesp_query as a string message response.
    resp_txt = json.dumps(resp_queries,indent=2,default=str)

    ## add this respnse to hist_nlp2sql.
    hist_nlp2sql.append({'role':'assistant','content':resp_txt})

    ## remoe evry other mesage type with roles ither than 'system'.
    temp = []
    for j in hist_nlp2sql:
        if j["role"] == "system":
            temp.append(j)

    hist_nlp2sql = temp


    return resp_txt











