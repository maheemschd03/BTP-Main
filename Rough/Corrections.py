from google import genai
from google.genai import types
from DB import run_query


client = genai.Client(api_key="AIzaSyCGRagRWD_XWzdlR6ZGgJfyeKZM6agwMw4")
config = types.GenerateContentConfig(tools=[run_query])

def AI(query):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{query}",
        config=config,
    )

    #print(response.text)
    return response.text


def convo():
    user = input("Enter the query : ")

    complete_command = f'''

    user = {user}

    Run an SQL command. also you can use always use sql quries to know the schema if unsure. like you can always use desc table_name etc.
    Always try to solve all the problems yourself first you have all the neccsary tools.



    '''

    AI(complete_command)
