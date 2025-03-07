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
with open(f"shared/score_calculator/score_examples.json", "r") as file:
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
             with one decimal place. 5.0 represents a low footprint while 0.0 represents a high footprint.
             
             ### EXAMPLES ###

             [{example_dict[json_name]["perfect_phone"]}] // 5.0
             [{example_dict[json_name]["low_end_phone"]}] // 0.0
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
    bat = scores[0]
    long = scores[1]
    rep = scores[2]
    prod = scores[3]
    rec = scores[4]
    co2 = scores[6]
    long = ((long + bat) / 2) - 2.5 # 1
    long = (long + rep) / 2         # 1.5
    long = max(0, long)             # 1.5
    neg1 = (5-prod) - 0.1 * rec - 0.5 * long   # 1.5   -0.45 - 0.75 =0.3
    neg1 = max(0, neg1)
    neg2 = 5- co2                   # 0.5
    t_score = 5- (neg1 + neg2)/2       # 0.8/2 = 0.4
    t_score = min(5.0, t_score)
    t_score = round(t_score, 1)
    return t_score

