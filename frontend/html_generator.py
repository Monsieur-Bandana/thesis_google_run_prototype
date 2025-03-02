# response = f"""<li class="{css_name}-css-class"><span style="font-weight: bold">{response_dic["generated_adj"]} {class_name}:</span> {response_dic["html_output"]}<span class="sources">{response_dic["footnotes_span"]}</span></li>"""

all_phones_scores = {}

def calc_ratio(json_name, score, is_in_score_list)->float:
    list_of_other_scores: list[float] = all_phones_scores[json_name]
    if is_in_score_list == "false":
        print("//////////////////////////////////////////////////////////////////////////////////////")
        list_of_other_scores.append(score)
    num_of_other_scores = 0
    for el in list_of_other_scores:
        if el <= score:
            num_of_other_scores+=1
    ouptut_t = (num_of_other_scores-1)/(len(list_of_other_scores)-1)
    return ouptut_t

def render_calc_text(ratio: float)->str:
    t:str = str(ratio * 100).split(".")[0]
    spaces_needed = 3-len(t)
    spaces = ""
    for i in range(0, spaces_needed):
        spaces+="&nbsp;&nbsp;"
    t=f"{spaces}{t}"
    print(t)
    return t

def render_calc_display(ratio:float, width=75):
    total_width = width
    return f"""
        <div class="ratio_container">
            <div class="outer_ratio" style="width: {total_width}px">
                <div class="inner_ratio" style="width: {total_width*ratio}px">

                </div>
            </div>
            <div class="arrow_placer" style="width: {total_width*ratio+9}px">
                &#9650;
            </div>
        </div>
    """

def create_header(title: str, score: float, json_name, is_in_score_list, add_key = True):

    ouptut_t = calc_ratio(json_name, score, is_in_score_list)

    addId = ""
    if add_key:
        addId = f"""id="{json_name}" """
    header_html = f"""
                    <div class="headline" {addId}>
                        <div class="span_alike"><span class="title_span">{title}</span></div>
                        <div class="span_alike">
                         
                            {color_leafs(score)}
                           
                            <div class="ratio-with-perc">
                                {render_calc_display(ouptut_t)}<span>{render_calc_text(ouptut_t)}%</span>
                            </div>
                        </div>
                    </div>
                  
    """
    return header_html 

def addTableEntry(title: str, json_name: str, score: float):

    header_html = f"""
                    <td style="width: 25%">
                        <a href="#{json_name}">{title}</a>
                    </td>
                    <td>
                        
                        {color_leafs(score, "black")}
                       
                    </td>
                    
    """
    return header_html   

def generate_table_output(resp1: dict, resp2: dict, all_phones_scores2: dict):
    is_in_score_list1 = resp1["in_list"]
    is_in_score_list2 = resp2["in_list"]     
    def create_td(diczt:dict, direction: str):
        print(diczt)
        td= f"""<td style="width: 50%; padding-{direction}: 3px;"><ul>"""
        cont=""
        
        for k, v in diczt.items():
            if k not in ["score", "name", "in_list"]:
                cont+=f"""
                        <li><span style="font-weight: bold">{v["adjective"]} {v["class_name"]}:</span> {v["summary"]}</li>
                    """
        cont+="</ul></td>"
        td+=cont

        return td
    
    def render_comparative_table(dicti: dict):
        def check_for_bigger(val1,val2):
            div=""
            if val1>=val2:
                div="""<i class="fa fa-leaf" style="color: white"></i>"""
            return div
        print(dicti)
        r1 = f"""<tr><td>Category</td><td>{dicti["name"]["0"]}</td><td>{dicti["name"]["1"]}</td></tr>"""
        t1 = dicti["conclusion"]["0"]["score"]
        t2 = dicti["conclusion"]["1"]["score"]
        ouptut_t1 = calc_ratio("total_score", t1, is_in_score_list1)
        ouptut_t2 = calc_ratio("total_score", t2, is_in_score_list2)

        r1 += f"""<tr style="font-size: 1.6rem"><td>Estimated total score</td><td>{color_leafs(t1, "black")}
                    <div class="ratio-with-perc">
                        {render_calc_display(ouptut_t1)}<span>{render_calc_text(ouptut_t1)}%</span>
                    </div>

                </td><td>{color_leafs(t2, "black")}
                    <div class="ratio-with-perc">
                        {render_calc_display(ouptut_t2)}<span>{render_calc_text(ouptut_t2)}%</span>
                    </div>
                </td></tr>
                """
        for key, val in dicti.items():
            if key not in ["conclusion", "name", "in_list"]:
                na = f"""<a href="#{key}">{val["0"]["name"]}</a>"""
                sc1 = val["0"]["score"]
                sc2 = val["1"]["score"]
                r1 += f"""<tr><td style="width: 30%">{na}</td><td style="width: 35%">{color_leafs(sc1, "black", check_for_bigger(sc1, sc2))}</td>
                                <td style="width: 35%">{color_leafs(sc2, "black", check_for_bigger(sc2, sc1))}</td></tr>"""
        return f"""<table style="width: 100%">{r1}</table>"""
    
    def render_header_row(key, dicti:dict, is_in_score_list2):
        ouptut = calc_ratio(key, dicti["score"], is_in_score_list2)
        sc = dicti["score"]

        r1 = f"""
                
                        <div class="span_alike">
                           
                            {color_leafs(sc)}
                           
                            <div class="ratio-with-perc">
                                {render_calc_display(ouptut)}<span>{render_calc_text(ouptut)}%</span>
                            </div>
                        </div>
            """
        return r1
    global all_phones_scores
    all_phones_scores = all_phones_scores2


    table = """<table style="width: 100%">"""
    new_resp = {}
    for key, val in resp1.items():
        new_resp[key] = {"0": val, "1": resp2[key]}
    
    cont_row = f"""<tr><td colspan="2">{render_comparative_table(new_resp)}</td></tr>"""
    table_content = ""
    first_row = f"""<tr><td>{new_resp["conclusion"]["0"]["summary"]}</td>
    <td>{new_resp["conclusion"]["1"]["summary"]}</td></tr>"""

    for key, val in new_resp.items():
        if key not in ["conclusion", "name", "in_list"]:
            
            header = f"""<tr id={key}><td colspan="2">
                            <div style="display: flex; justify-content: space-between; color: white">
                                <div class="span_alike"><span class="title_span">{val["0"]["name"]}</span></div>
                                {render_header_row(key, val["0"], is_in_score_list1)}{render_header_row(key, val["1"], is_in_score_list2)}</div>
                        </td></tr>
                    """

            ## header durchgehend, für score and ration jeweils in einer zeile
            row=f"""{header}<tr> {create_td(val["0"], "right")}{create_td(val["1"], "left")}</tr>"""

            table_content +=row

    final_response=f"""{table}{cont_row}{first_row}{table_content}</table>"""

    return final_response



def generate_html_output(resp: dict, all_phones_scores2: dict, is_in_scorelsit = True):
    global all_phones_scores
    all_phones_scores = all_phones_scores2

    is_in_score_list = resp["in_list"]
    final_response = ""
    tablecounter = 0
    table = """<table style="width: 100%">"""
    print("*******************************************************")
    print(resp)
    for key, val in resp.items():
        if key not in ["conclusion", "name", "in_list"]:
            h_ = create_header(title=val["name"], json_name=key, score=val["score"], is_in_score_list=is_in_score_list)
            if tablecounter%2==0:
                table = table + f"<tr>{addTableEntry(title=val["name"], json_name=key, score=val["score"])}"
            else:
                table = table + f"{addTableEntry(title=val["name"], json_name=key, score=val["score"])}</tr>"
            tablecounter += 1
            final_response += h_
            sub_dic_list: dict = val
            final_response += "<ul>"
            for k, v in sub_dic_list.items():
                # el_dict: dict = next(iter(el.values()))
                if type(v) == dict:
                    line = f"""
                        <li><span style="font-weight: bold">{v["adjective"]} {v["class_name"]}:</span> {v["summary"]}</li>
                    """
                    final_response += line

            final_response += "</ul>"
    if not table.endswith("</tr>"):
        table = table + "</tr>"

    table = table + "</table>"
    final_response = generate_conclusional_header(conclusion=resp["conclusion"]["summary"], table = table, total_score=resp["conclusion"]["score"], is_in_score_list=is_in_score_list) + final_response
        

    return final_response

def generate_conclusional_header(conclusion, total_score: float, table,is_in_score_list):
    output_t = calc_ratio("total_score", total_score, is_in_score_list)
    header = f"""<div class="t-header">
                    <div class="t-frame">
                        <span>Estimated score</span>
                        <span class="score_span">
                            {color_leafs(total_score, "black")}
                        </span>
                    </div>
                    <div class="t-ratio">
                        <div style="width: 180px">
                            {render_calc_display(output_t, 200)}
                            <div class="t-ratio-corrector">
                                equal or better score than of {str(output_t * 100).split(".")[0]}% of phones on this plattform
                            </div>
                        </div>
                    </div>
                </div>"""
    final_resp = f"""{header}{table}
    <div style="display: flex; justify-content: flex-end;">
        <div>
            <i class="fa fa-info-circle"></i> Press the links for getting further insights!
        </div>
    </div>
    <div style="display: block; margin-top: 15px">{conclusion}</div>
    <div class="t-header" style="height: 50px; justify-content: center;">
        <div class="t-frame">
            <span>Fulltext reviews:</span>
        </div>
    </div>
    """
    return final_resp

def color_leafs(score: float, default_color="white", add_ons = ""):
    color = "green"
    if score < 4.0:
        color = "rgb(138, 193, 107)"
    if score < 3.0:
        color = "rgb(242, 140, 40)"
    if score < 2.0:
        color = "rgb(159 101 78)"
    returnhtml: str = ""
    scd_digit = score%1
    first_digit = score-scd_digit
    first_digit = int(first_digit)
    for i in range(0, first_digit):
        returnhtml = returnhtml + f"""<i class="fa fa-leaf" style="color: {color}"></i>"""
    if first_digit < 5:
        border_percent = int(scd_digit * 100)
        relative_icon = f"""<i class="fa fa-leaf" style="background: linear-gradient(to right, {color} 0% {str(border_percent)}%, {default_color} {str(border_percent)}% 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i>"""
        returnhtml = returnhtml + relative_icon
    for i in range(first_digit + 1 , 5):
        returnhtml += f"""<i class="fa fa-leaf" style="color: {default_color}"></i>"""
    add_html = ""
    if score == 5.0:
        add_html += "color: green; "
    returnhtml=f"""<div style="{add_html}">{returnhtml} {score} {add_ons}</div>"""
    return returnhtml

# print(color_leafs(4.0))
"""
dicti: dict = {
    'materials': {
        'metals': {
            'summary': 'The iPhone 16 utilizes metals such as aluminum, cobalt, lithium, and rare earth elements like neodymium and tungsten. Apple has made significant strides in incorporating recycled materials, with over 30% of recycled content across various components, including 100% recycled aluminum in the thermal substructure and 100% recycled cobalt and lithium in the battery.',
            'adjective': 'recycled and essential',
            'class_name': "Couldn't find name"
        },
        'chemicals': {
            'summary': 'Toxic chemicals present in the iPhone 16 include brominated flame retardants, PVC, and phthalates, which are used for insulation and durability. Apple has moved towards safer chemistry, ensuring that the iPhone 16 is free from harmful substances like arsenic and mercury, and is working to eliminate PVC and phthalates in its products.',
            'adjective': 'hazardous but improving',
            'class_name': "Couldn't find name"
        },
        'origin': {
            'summary': 'Natural resources for the iPhone 16 are sourced globally, with rare earth elements primarily mined in China, Australia, and the Democratic Republic of the Congo. This sourcing raises environmental concerns related to habitat destruction and pollution, but Apple is committed to responsible sourcing practices and mapping materials back to their mineral sources.',
            'adjective': 'global and impactful',
            'class_name': "Couldn't find name"
        },
        'name': 'Materials',
        'score': 3.5
    },
    'transportation': {
        'transportation': {
            'summary': 'The iPhone 16 components are manufactured in various countries before being assembled in China, leading to substantial transportation distances that contribute to carbon emissions. Apple is actively working to minimize transport distances and is transitioning towards low-carbon transport methods to reduce the environmental impact.',
            'adjective': 'extensive and carbon-intensive',
            'class_name': "Couldn't find name"
        },
        'name': 'Transportation',
        'score': 3.0
    },
    'production': {
        'production_process': {
            'summary': 'The production of the iPhone 16 involves extracting raw materials, manufacturing components like printed circuit boards, and final assembly. Apple emphasizes sustainability through its Supplier Clean Energy Program, mandating renewable energy usage and optimizing manufacturing processes to minimize waste and emissions.',
            'adjective': 'complex and evolving',
            'class_name': "Couldn't find name"
        },
        'production_waste': {
            'summary': 'The manufacturing process generates significant waste, including defective components and excess materials. Apple employs rigorous waste management strategies, aiming for zero waste to landfill across its facilities and focusing on recycling and reusing materials to mitigate environmental impact.',
            'adjective': 'substantial and managed',
            'class_name': "Couldn't find name"
        },
        'supplier_energy_use': {
            'summary': 'Energy consumption at production sites is significant, with Apple pushing for renewable energy. Over 320 suppliers have committed to using 100% renewable electricity, which helps reduce reliance on fossil fuels and lowers greenhouse gas emissions associated with production.',
            'adjective': 'high and renewable',
            'class_name': "Couldn't find name"
        },
        'location_of_assembly': {
            'summary': 'Assembly sites for the iPhone 16 are primarily located in China, chosen for cost efficiency. However, this can lead to concerns about weaker environmental regulations in these regions. Apple ensures compliance with strict environmental and labor standards at its assembly locations.',
            'adjective': 'cost-efficient but regulated',
            'class_name': "Couldn't find name"
        },
        'name': 'Production',
        'score': 3.5
    },
    'use': {
        'ease_of_reparation': {
            'summary': 'Repairing the iPhone 16 can be challenging due to proprietary parts and assembly methods. While Apple has made efforts to improve repairability by increasing parts availability and providing manuals, the complexity still hinders easy user repairs, contributing to e-waste.',
            'adjective': 'challenging and improving',
            'class_name': "Couldn't find name"
        },
        'ease_of_modification': {
            'summary': 'The iPhone 16 offers limited options for hardware performance upgrades, as Apple controls significant aspects of hardware and software functionality. This limitation can lead to increased demand for new devices rather than upgrades, contributing to environmental impact.',
            'adjective': 'limited and restrictive',
            'class_name': "Couldn't find name"
        },
        'top_notch_technology': {
            'summary': 'The iPhone 16 meets high technological standards, promoting longevity and decreasing the likelihood of early replacements. By incorporating cutting-edge technology, Apple aims to reduce the environmental impact by extending the product lifecycle.',
            'adjective': 'advanced and sustainable',
            'class_name': "Couldn't find name"
        },
        'quality_of_battery': {
            'summary': 'Batteries in the iPhone 16 are designed for durability, typically lasting around 2-3 years before performance degradation occurs. However, they are not user-replaceable, which can contribute to e-waste when batteries fail.',
            'adjective': 'durable but non-replaceable',
            'class_name': "Couldn't find name"
        },
        'name': 'Use',
        'score': 3.5
    },
    'end_of_life': {
        'planned_obsolescence': {
            'summary': "Concerns about planned obsolescence have been raised regarding Apple's software updates that may reduce performance in older models. While Apple does not explicitly employ planned obsolescence, this practice can lead to increased electronic waste as users may feel pressured to upgrade.",
            'adjective': 'controversial and debated',
            'class_name': "Couldn't find name"
        },
        'second_use': {
            'summary': 'The likelihood of the iPhone 16 being sold or reused after its initial use is relatively high, supported by strong resale and refurbishment programs like Apple Trade-In. The quality retention of iPhones contributes to their potential for reuse, which can lessen the environmental footprint.',
            'adjective': 'promising and supported',
            'class_name': "Couldn't find name"
        },
        'recycling': {
            'summary': 'Apple has made significant progress in facilitating recycling, with many components designed for recyclability. However, actual recycling rates remain low due to consumer behavior and infrastructure challenges. Apple is scaling up its recycling efforts to enhance recovery rates and improve sustainability.',
            'adjective': 'potential and improving',
            'class_name': "Couldn't find name"
        },
        'name': 'End of Life',
        'score': 3.5
    },
    'conclusion': {
        'summary': 'The carbon footprint of the iPhone 16 is influenced by significant material sourcing, manufacturing processes, and transportation distances, all contributing to emissions. While Apple focuses on renewable energy and recycling efforts, challenges like e-waste and complex repairability suggest a negative impact on the environmental footprint overall.',
        'score': 3.3
    }
}

dicti2: dict = {
    'materials': {
        'metals': {
            'summary': 'The iPhone 16 utilizes metals such as aluminum, cobalt, lithium, and rare earth elements like neodymium and tungsten. Apple has made significant strides in incorporating recycled materials, with over 30% of recycled content across various components, including 100% recycled aluminum in the thermal substructure and 100% recycled cobalt and lithium in the battery.',
            'adjective': 'recycled and essential',
            'class_name': "Couldn't find name"
        },
        'chemicals': {
            'summary': 'Toxic chemicals present in the iPhone 16 include brominated flame retardants, PVC, and phthalates, which are used for insulation and durability. Apple has moved towards safer chemistry, ensuring that the iPhone 16 is free from harmful substances like arsenic and mercury, and is working to eliminate PVC and phthalates in its products.',
            'adjective': 'hazardous but improving',
            'class_name': "Couldn't find name"
        },
        'origin': {
            'summary': 'Natural resources for the iPhone 16 are sourced globally, with rare earth elements primarily mined in China, Australia, and the Democratic Republic of the Congo. This sourcing raises environmental concerns related to habitat destruction and pollution, but Apple is committed to responsible sourcing practices and mapping materials back to their mineral sources.',
            'adjective': 'global and impactful',
            'class_name': "Couldn't find name"
        },
        'name': 'Materials',
        'score': 4.5
    },
    'transportation': {
        'transportation': {
            'summary': 'The iPhone 16 components are manufactured in various countries before being assembled in China, leading to substantial transportation distances that contribute to carbon emissions. Apple is actively working to minimize transport distances and is transitioning towards low-carbon transport methods to reduce the environmental impact.',
            'adjective': 'extensive and carbon-intensive',
            'class_name': "Couldn't find name"
        },
        'name': 'Transportation',
        'score': 2.0
    },
    'production': {
        'production_process': {
            'summary': 'The production of the iPhone 16 involves extracting raw materials, manufacturing components like printed circuit boards, and final assembly. Apple emphasizes sustainability through its Supplier Clean Energy Program, mandating renewable energy usage and optimizing manufacturing processes to minimize waste and emissions.',
            'adjective': 'complex and evolving',
            'class_name': "Couldn't find name"
        },
        'production_waste': {
            'summary': 'The manufacturing process generates significant waste, including defective components and excess materials. Apple employs rigorous waste management strategies, aiming for zero waste to landfill across its facilities and focusing on recycling and reusing materials to mitigate environmental impact.',
            'adjective': 'substantial and managed',
            'class_name': "Couldn't find name"
        },
        'supplier_energy_use': {
            'summary': 'Energy consumption at production sites is significant, with Apple pushing for renewable energy. Over 320 suppliers have committed to using 100% renewable electricity, which helps reduce reliance on fossil fuels and lowers greenhouse gas emissions associated with production.',
            'adjective': 'high and renewable',
            'class_name': "Couldn't find name"
        },
        'location_of_assembly': {
            'summary': 'Assembly sites for the iPhone 16 are primarily located in China, chosen for cost efficiency. However, this can lead to concerns about weaker environmental regulations in these regions. Apple ensures compliance with strict environmental and labor standards at its assembly locations.',
            'adjective': 'cost-efficient but regulated',
            'class_name': "Couldn't find name"
        },
        'name': 'Production',
        'score': 5.5
    },
    'use': {
        'ease_of_reparation': {
            'summary': 'Repairing the iPhone 16 can be challenging due to proprietary parts and assembly methods. While Apple has made efforts to improve repairability by increasing parts availability and providing manuals, the complexity still hinders easy user repairs, contributing to e-waste.',
            'adjective': 'challenging and improving',
            'class_name': "Couldn't find name"
        },
        'ease_of_modification': {
            'summary': 'The iPhone 16 offers limited options for hardware performance upgrades, as Apple controls significant aspects of hardware and software functionality. This limitation can lead to increased demand for new devices rather than upgrades, contributing to environmental impact.',
            'adjective': 'limited and restrictive',
            'class_name': "Couldn't find name"
        },
        'top_notch_technology': {
            'summary': 'The iPhone 16 meets high technological standards, promoting longevity and decreasing the likelihood of early replacements. By incorporating cutting-edge technology, Apple aims to reduce the environmental impact by extending the product lifecycle.',
            'adjective': 'advanced and sustainable',
            'class_name': "Couldn't find name"
        },
        'quality_of_battery': {
            'summary': 'Batteries in the iPhone 16 are designed for durability, typically lasting around 2-3 years before performance degradation occurs. However, they are not user-replaceable, which can contribute to e-waste when batteries fail.',
            'adjective': 'durable but non-replaceable',
            'class_name': "Couldn't find name"
        },
        'name': 'Use',
        'score': 3.5
    },
    'end_of_life': {
        'planned_obsolescence': {
            'summary': "Concerns about planned obsolescence have been raised regarding Apple's software updates that may reduce performance in older models. While Apple does not explicitly employ planned obsolescence, this practice can lead to increased electronic waste as users may feel pressured to upgrade.",
            'adjective': 'controversial and debated',
            'class_name': "Couldn't find name"
        },
        'second_use': {
            'summary': 'The likelihood of the iPhone 16 being sold or reused after its initial use is relatively high, supported by strong resale and refurbishment programs like Apple Trade-In. The quality retention of iPhones contributes to their potential for reuse, which can lessen the environmental footprint.',
            'adjective': 'promising and supported',
            'class_name': "Couldn't find name"
        },
        'recycling': {
            'summary': 'Apple has made significant progress in facilitating recycling, with many components designed for recyclability. However, actual recycling rates remain low due to consumer behavior and infrastructure challenges. Apple is scaling up its recycling efforts to enhance recovery rates and improve sustainability.',
            'adjective': 'potential and improving',
            'class_name': "Couldn't find name"
        },
        'name': 'End of Life',
        'score': 3.5
    },
    'conclusion': {
        'summary': 'The carbon footprint of the iPhone 16 is influenced by significant material sourcing, manufacturing processes, and transportation distances, all contributing to emissions. While Apple focuses on renewable energy and recycling efforts, challenges like e-waste and complex repairability suggest a negative impact on the environmental footprint overall.',
        'score': 8.3
    }
}

# print(generate_html_output(dicti))
print(generate_table_output(dicti, dicti2, []))

"""