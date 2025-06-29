import os
from google import genai
from google.genai import types

# Set your API key here
os.environ["genai"] = "add your API"

def generate(prompt):
    client = genai.Client(
        api_key=os.environ.get("genai"),
    )

    model = "gemma-3-27b-it"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    return response.text
    # print(response.text)

# Example usage
# generate("hi whats up")
#