from openai import OpenAI
from shared.ind_key import rand_k
import os
import json
from google.cloud import storage
from google.api_core.exceptions import NotFound
from shared.gcs_handler import download_file_from_bucket, create_temp_folder
from shared.git_handler import load_class_data_from_git
from shared.test_center import conclusion_tester
import random

from pydantic import BaseModel

class AnswerWithReasoning(BaseModel):
    score: float
    reasoning: str

sk = rand_k
client = OpenAI(api_key=sk)

def generate_score(respones: list[dict]):

    context: str = " "
    for el in respones:
        context = context + el["html_output"]
    """
    prompt=f"{context}\nPress Enter to continue..."
    input(prompt)
    """
    question = f"""Based on the context, which you find within the input-brackets, rate the environmental footprint. The ouput is a single double value with one decimal place.
    5.0 represents a low footprint while 1.0 represents a high footprint.
    <input>{context}</input>
    Further add a justification how you came to the score
    Convert your response into the given structure.
    """
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that responds only with a single double value with one decimal place."},
            {
                "role": "user",
                "content": question
            }
        ],
        response_format=AnswerWithReasoning
    )
    
    generated_text = completion.choices[0].message.content
    generated_answer_dict:dict = json.loads(generated_text)
    

    return generated_answer_dict["score"]

