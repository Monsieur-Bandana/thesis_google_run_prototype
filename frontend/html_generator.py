# response = f"""<li class="{css_name}-css-class"><span style="font-weight: bold">{response_dic["generated_adj"]} {class_name}:</span> {response_dic["html_output"]}<span class="sources">{response_dic["footnotes_span"]}</span></li>"""

def create_header(title: str, json_name: str, score: float):
    add_html = ""
    if score == 5.0:
        add_html = """style= "color: green" """
    header_html = f"""
                    <div class="headline" id="{json_name}">
                        <span class="title_span">{title}</span>
                        <span class="score_span" {add_html}>
                        {color_leafs(score)}
                        {str(score)}
                        </span>
                    </div>
                  
    """
    return header_html 

def addTableEntry(title: str, json_name: str, score: float):
    add_html = ""
    if score == 5.0:
        add_html = """style= "color: green" """
    header_html = f"""
                    <td>
                        <a href="#{json_name}">{title}</a>
                    </td>
                    <td>
                        <span {add_html}>
                        {color_leafs(score, "black")}
                        {str(score)}
                        </span>
                    </td>
                    
    """
    return header_html       

def generate_html_output(resp: dict):
    final_response = ""
    tablecounter = 0
    table = """<table style="width: 100%">"""
    for key, val in resp.items():
        if key not in ["conclusion", "name"]:
            h_ = create_header(title=val["name"], json_name=key, score=val["score"])
            if tablecounter%2==0:
                table = table + f"<tr>{addTableEntry(title=val["name"], json_name=key, score=val["score"])}"
            else:
                table = table + f"{addTableEntry(title=val["name"], json_name=key, score=val["score"])}</tr>"
            tablecounter = tablecounter + 1
            final_response = final_response + h_
            sub_dic_list: dict = val
            final_response = final_response + "<ul>"
            for k, v in sub_dic_list.items():
                # el_dict: dict = next(iter(el.values()))
                if type(v) == dict:
                    line = f"""
                        <li><span style="font-weight: bold">{v["adjective"]} {k}:</span> {v["summary"]}</li>
                    """
                    final_response = final_response + line

            final_response = final_response + "</ul>"
    if not table.endswith("</tr>"):
        table = table + "</tr>"

    table = table + "</table>"
    final_response = generate_conclusional_header(conclusion=resp["conclusion"]["summary"], table = table, total_score=resp["conclusion"]["score"]) + final_response
        

    return final_response

def generate_conclusional_header(conclusion, total_score: float, table):
    header = f"""<div class="t-header">
                    <div class="t-frame">
                        <span>Estimated score</span>
                        <span class="score_span">
                            {color_leafs(total_score, "black")}
                            {str(total_score)}
                        </span>
                    </div>
                </div>"""
    final_resp = f"""{header}{table}<div style="display: block"><p>{conclusion}</p>Further Details:</div>"""
    return final_resp

def color_leafs(score: float, default_color="white"):
    color = "green"
    if score < 4.0:
        color = "rgb(138, 193, 107)"
    if score < 3.0:
        color = "rgb(242, 140, 40)"
    if score < 2.0:
        color = "rgb(104, 53, 33)"
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
        returnhtml = returnhtml + f"""<i class="fa fa-leaf" style="color: {default_color}"></i>"""
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
"""
# print(generate_html_output(dicti))
