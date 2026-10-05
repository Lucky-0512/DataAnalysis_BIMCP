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

## get schema content.
with open("./sys_prompts/dbSchema.txt","r") as schemaFile:
    content = schemaFile.read()

## let's get the skills prompt.
with open("./sys_prompts/skills.txt","r") as skillFile:
    skills = skillFile.read()

# now let's set the postgres knowledge base prompt.
with open("./sys_prompts/postgresql_knowledge_base.txt","r") as knowledge:
    know = knowledge.read()

## define the first rigger pipeline.("NLP TO SQL I mean it => sql generator model.")

with open("./sys_prompts/instruct_prompt.txt","a") as kk:
    kk.write(skills)






