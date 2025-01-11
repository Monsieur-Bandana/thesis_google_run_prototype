from openai import OpenAI
from shared.ind_key import rand_k
import json
from pydantic import BaseModel

class AnswerWithReasoning(BaseModel):
    score: float
    reasoning: str

sk = rand_k
client = OpenAI(api_key=sk)

def generate_score(respones: list[dict])->dict:

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
    

    return generated_answer_dict

def get_total_score(scores:list[float]):
    t_score=5-0.83*(5-scores[0])-0.2*(5-scores[1])-0.15*(5-scores[2])+0.06*scores[4]
    t_score = round(t_score, 1)
    return t_score