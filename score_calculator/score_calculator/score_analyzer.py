from openai import OpenAI
from shared.ind_key import rand_k
import json
from pydantic import BaseModel


class AnswerWithReasoning(BaseModel):
    score: float
    reasoning: str

sk = rand_k
client = OpenAI(api_key=sk)
example_dict:dict = {}
with open(f"score_calculator/score_calculator/score_examples.json", "r") as file:
        example_dict = json.load(file)


def generate_score(respone: str, json_name)->float:

    """
    context: str = " "
    for el in respones:
        context = context + el["html_output"]
    prompt=f"{context}\nPress Enter to continue..."
    input(prompt)
    """

    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"""You are a helpful assistant, rating the environmental footprint of smartphones based on input texts. You give ratings in float format
             with one decimal place. 5.0 represents a low footprint while 1.0 represents a high footprint.
             
             ### EXAMPLES ###

             [{example_dict[json_name]["perfect_phone"]}] // 5.0
             [{example_dict[json_name]["low_end_phone"]}] // 1.0
             [{example_dict[json_name]["mid"]}] // 2.0
             
             """},
            {
                "role": "user",
                "content": f"[{respone}] //"
            }
            
        ],
        max_tokens=3,
        temperature=0
    )
    
    generated_text = completion.choices[0].message.content
    # print(generated_text)
    float_value = float(generated_text)

    return float_value

def get_total_score(scores:list[float]):
    t_score=5-0.83*(5-scores[0])-0.2*(5-scores[1])-0.15*(5-scores[2])+0.06*scores[4]
    t_score = round(t_score, 1)
    return t_score

