# response = f"""<li class="{css_name}-css-class"><span style="font-weight: bold">{response_dic["generated_adj"]} {class_name}:</span> {response_dic["html_output"]}<span class="sources">{response_dic["footnotes_span"]}</span></li>"""


def generate_html_output(resp: list[dict], parent: dict, score: float):
    header_html = f"""
                    <div class="headline" id="{parent["json_name"]}">
                        <span class="title_span">{parent["name"]}</span>
                        <span class="score_span">
                            <i class="fa fa-leaf"></i>
                            <i class="fa fa-leaf"></i>
                            <i class="fa fa-leaf"></i>
                            <i class="fa fa-leaf"></i>
                            <i class="fa fa-leaf"></i>
                        {str(score)}</span>
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