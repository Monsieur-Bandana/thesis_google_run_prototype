# response = f"""<li class="{css_name}-css-class"><span style="font-weight: bold">{response_dic["generated_adj"]} {class_name}:</span> {response_dic["html_output"]}<span class="sources">{response_dic["footnotes_span"]}</span></li>"""


def generate_html_output(resp: list[dict], parent: dict, score_dict: dict):
    score = score_dict["score"]
    reasoning = score_dict["reasoning"]
    header_html = f"""
                    <div class="headline" id="{parent["json_name"]}">
                        <span class="title_span">{parent["name"]}</span>
                        <span class="score_span">
                        {color_leafs(score)}
                        {str(score)}
                        <div class="tooltiptext">{reasoning}</div>
                        </span>
                    </div>
    """
    final_response = "<ul>"
    for r in resp:
        line = f"""
            <li><span style="font-weight: bold">{r["generated_adj"]} {r["class_name"]}:</span> {r["html_output"]}<span class="sources">{r["footnotes_span"]}</span></li>
        """
        final_response = final_response + line
    final_response = final_response + "</ul>"
    final_response = header_html + final_response
    return final_response

def generate_final_answer(conclusion, context, total_score: float):
    header = f"""<div class="t-header">
                    <div class="t-frame">
                        <span>Estimated score</span>
                        <span class="score_span">
                            {color_leafs(total_score, "black")}
                            {str(total_score)}
                        </span>
                    </div>
                </div>"""
    final_resp = f"""{header}<div style="display: block"><p>{conclusion}</p>Further Details:</div>{context}"""
    return final_resp

def color_leafs(score: float, default_color="white"):
    returnhtml: str = ""
    scd_digit = score%1
    first_digit = score-scd_digit
    first_digit = int(first_digit)
    for i in range(0, first_digit):
        returnhtml = returnhtml + """<i class="fa fa-leaf" style="color: green"></i>"""
    border_percent = int(scd_digit * 100)
    relative_icon = f"""<i class="fa fa-leaf" style="background: linear-gradient(to right, green 0% {str(border_percent)}%, {default_color} {str(border_percent)}% 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i>"""
    returnhtml = returnhtml + relative_icon
    for i in range(first_digit + 1 , 5):
        returnhtml = returnhtml + f"""<i class="fa fa-leaf" style="color: {default_color}"></i>"""
    return returnhtml

# print(color_leafs(4.0))