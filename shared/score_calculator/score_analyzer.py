from openai import OpenAI
from shared.ind_key import rand_k
import json
from pydantic import BaseModel


class AnswerWithReasoning(BaseModel):
    score: float
    reasoning: str


sk = rand_k
client = OpenAI(api_key=sk)
example_dict: dict = {}
with open(f"shared/score_calculator/score_examples.json", "r") as file:
    example_dict = json.load(file)


def check_for_further(key, json_name):
    return_str = ""
    rating = ""
    if key == "low_mid":
        rating = 2.0
    elif key == "high_mid":
        rating = 4.0
    try:
        return_str = f"""[{example_dict[json_name][key]}] // {rating}"""
    except:
        print(f"No {key}-data given")
    return return_str


def generate_score(respone: str, json_name) -> float:
    """
    context: str = " "
    for el in respones:
        context = context + el["html_output"]
    prompt=f"{context}\nPress Enter to continue..."
    input(prompt)
    """
    print(example_dict[json_name]["perfect_phone"])
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""You are a helpful assistant, rating the environmental footprint of smartphones based on input texts. You give ratings in float format
             with one decimal place. 5.0 represents a low footprint while 0.0 represents a high footprint.
             
             ### EXAMPLES ###

            [{example_dict[json_name]["perfect_phone"]}] // 5.0
            [{example_dict[json_name]["low_end_phone"]}] // 0.0
            [{example_dict[json_name]["mid"]}] // 2.5
            {check_for_further("low_mid", json_name)}
            {check_for_further("high_mid", json_name)}
             
             """,
            },
            {"role": "user", "content": f"[{respone}] //"},
        ],
        max_tokens=3,
        temperature=0,
    )

    generated_text = completion.choices[0].message.content
    # print(generated_text)
    float_value = float(generated_text)

    return float_value


def get_total_score(scores: list[float]):
    print("i was executed")
    bat = scores[0]
    long = scores[1]
    rep = scores[2]
    prod = scores[3]
    rec = scores[4]
    co2 = scores[6]
    long = (long + bat + rep) / 3  # 3.3
    long = long / 2.5  # 1.32
    long = max(0.1, long)  # 1.32
    neg1 = ((5 - prod) - 0.1 * rec) / long  # 2.6/1.32 =2
    neg1 = max(0, neg1)
    neg2 = 5 - co2  # 3
    t_score = 5 - (neg1 + neg2) / 2  # 5-2.5
    t_score = max(min(5.0, t_score), 0.0)
    t_score = round(t_score, 1)
    return t_score
