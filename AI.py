from google import genai
from google.genai import types
from DB import run_query

client = genai.Client(api_key="AIzaSyBJsGsTILf96oxFBhZkmyUZOGY_hLt3j2E")
config = types.GenerateContentConfig(tools=[run_query])


def AI(query):
    # Start the conversation
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config=config,
    )

    # Check if the response contains function calls
    while response.function_calls:
        # Execute each function call
        print(response.text)
        for function_call in response.function_calls:
            func_name = function_call.name
            args = function_call.args

            # Execute the function
            if func_name == "run_query":
                result = run_query(**args)
            else:
                result = f"Error: Unknown function {func_name}"

            # Send the function result back to the model
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[query, response, types.Part(function_response=types.FunctionResponse(
                    name=func_name,
                    response={"result": result}
                ))],
                config=config,
            )

    # Now the response should contain text
    return response.text
