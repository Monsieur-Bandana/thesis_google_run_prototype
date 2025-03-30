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
    """
    in some cases we have more than three few-shots, this method checks if we have further, and appends them to the prompt
    """
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

    print(example_dict[json_name]["perfect_phone"])
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        # API calls for score calculation, using few shots
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
    # match variables from scores list elements (innovation variable gets ignored)
    bat = scores[0]
    long = scores[1]
    rep = scores[2]
    prod = scores[3]
    rec = scores[4]
    co2 = scores[6]
    long = (long + bat + rep) / 3  # calc average for longevity
    long = (
        long / 2.5
    )  # normalize longevity value (normal phone has value 1), env-friendly phone 0.5 -> reduces footprint by halve
    long = max(0.1, long)  # prevent dividing by 0
    neg1 = (
        (5 - prod) - 0.1 * rec
    ) / long  # production costs - recycling and then divided by longevity
    neg1 = max(0, neg1)  # avoid negative numbers
    neg2 = 5 - co2  # calc co2 costs
    t_score = 5 - (neg1 + neg2) / 2  # calc total score
    t_score = max(min(5.0, t_score), 0.0)  # avoid numbers < 0 or > 5
    t_score = round(t_score, 1)
    return t_score
