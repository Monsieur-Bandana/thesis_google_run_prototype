import json
from shared.score_calculator.score_analyzer import generate_score, get_total_score
from shared.json_processor import create_json_file


def add_entry_to_all_scores_list(all_scores, key, score, save_file1, isLocPhone: bool):
    if not isLocPhone:
        try:
            all_scores[key].append(score)
        except:
            all_scores[key] = [score]
            print("")
        with open(save_file1, "w") as file:
            json.dump(all_scores, file, indent=4)


def _ex(response_dic: dict, sourcefolder: str, isLocPhone=False):
    scores_list: list[float] = []

    for key, val in response_dic.items():
        print(key)
        if isinstance(val, dict) and key != "conclusion":
            smaller_dict: dict = val
            text: str = ""
            for key2, val2 in smaller_dict.items():
                if not key2 == "name":
                    try:
                        text = text + val2["summary"]
                    except:
                        print(f"--------------->problem with {val2}")
            score: float = generate_score(text, key)

            response_dic[key]["score"] = score
            scores_list.append(score)
    total_score = get_total_score(scores_list)
    response_dic["conclusion"]["score"] = total_score
    if not isLocPhone:
        save_file = f"{sourcefolder}/temp/generated_reviews_with_score.json"
        create_json_file(response_dic, "", save_file)
    if isLocPhone:
        return response_dic


"""
resp_dic = {
        "materials": {
            "metals": {
                "summary": "The Fairphone 5 utilizes metals like cobalt, copper, aluminum, gold, and lithium, which are essential for its electronic components and batteries. The use of these metals contributes to the phone's functionality but also raises environmental concerns due to the ecological impacts associated with their extraction. Fairphone has improved by integrating over 70% fair or recycled materials in its production, including cobalt sourced under better working conditions and 100% Fairtrade gold.",
                "adjective": "essential but impactful",
                "class_name": "Couldn't find name"
            },
            "chemicals": {
                "summary": "Toxic chemicals such as lead, mercury, cadmium, and certain phthalates are present in Fairphone 5 components, commonly used for their electrical properties. These chemicals pose environmental risks during disposal or recycling. Fairphone aims to reduce the use of harmful substances and promote safer materials in its production processes.",
                "adjective": "hazardous and regulated",
                "class_name": "Couldn't find name"
            },
            "origin": {
                "summary": "Natural resources for the Fairphone 5 are sourced from various global mines, including cobalt from the Democratic Republic of Congo and rare earth elements from China. This sourcing raises ethical and environmental concerns related to labor practices and ecological degradation. Fairphone is committed to improving supply chain transparency and responsible sourcing to mitigate these issues.",
                "adjective": "global but problematic",
                "class_name": "Couldn't find name"
            },
            "name": "Materials"
        },
        "transportation": {
            "transportation": {
                "summary": "The Fairphone 5 components travel extensive distances from mines to manufacturing plants primarily in Asia, followed by assembly in Europe. This international shipping contributes significantly to the carbon footprint due to fossil fuel emissions. Fairphone is working to streamline logistics and reduce transportation distances where possible to lessen environmental impact.",
                "adjective": "distant and carbon-intensive",
                "class_name": "Couldn't find name"
            },
            "name": "Transportation"
        },
        "production": {
            "production_process": {
                "summary": "The production of Fairphone 5 involves extracting raw materials, refining them, and manufacturing components like printed circuit boards, culminating in final assembly. Fairphone emphasizes sustainable practices by utilizing low-energy production methods and modular designs to enhance repairability and recyclability, thereby minimizing waste and resource consumption.",
                "adjective": "resource-intensive but improving",
                "class_name": "Couldn't find name"
            },
            "production_waste": {
                "summary": "The manufacturing process of the Fairphone 5 generates electronic waste and materials scrap, although exact figures are not specified. Fairphone aims to manage this waste through recycling programs and efficient resource use, striving for a closed-loop system to reduce landfill contributions and promote material reuse.",
                "adjective": "significant but managed",
                "class_name": "Couldn't find name"
            },
            "supplier_energy_use": {
                "summary": "Fairphone collaborates with suppliers to ensure energy consumption during production is minimized and increasingly sourced from renewable energy. While specific energy consumption details are not provided, the focus on clean energy aims to limit greenhouse gas emissions associated with manufacturing.",
                "adjective": "variable but renewable",
                "class_name": "Couldn't find name"
            },
            "location_of_assembly": {
                "summary": "Assembly of the Fairphone 5 occurs primarily in Europe, chosen for adherence to higher labor standards. However, some components may still be assembled in Asia for cost efficiency, which can lead to weaker environmental regulations. Fairphone seeks to balance cost and ethical manufacturing practices in its assembly decisions.",
                "adjective": "strategic but cost-driven",
                "class_name": "Couldn't find name"
            },
            "name": "Production"
        },
        "use": {
            "ease_of_reparation": {
                "summary": "The Fairphone 5 is designed for easy repair, featuring modular components that users can replace with minimal tools. This design significantly reduces electronic waste by allowing users to extend the device's lifespan through repairs rather than complete replacements, promoting sustainability.",
                "adjective": "user-friendly and sustainable",
                "class_name": "Couldn't find name"
            },
            "ease_of_modification": {
                "summary": "Users can upgrade components such as batteries and cameras in the Fairphone 5, which supports longevity by discouraging the frequent replacement of entire devices. This capability enhances the phone's sustainability by enabling users to adapt their devices to their needs over time.",
                "adjective": "flexible and sustainable",
                "class_name": "Couldn't find name"
            },
            "top_notch_technology": {
                "summary": "The Fairphone 5 is equipped with modern technological specifications that meet current market standards, reducing the likelihood of premature obsolescence. By ensuring competitive performance, Fairphone aims to minimize the need for users to replace their devices frequently, contributing positively to the environmental footprint.",
                "adjective": "advanced and enduring",
                "class_name": "Couldn't find name"
            },
            "quality_of_battery": {
                "summary": "The battery in the Fairphone 5 is designed for longevity, with a capacity of 4200mAh and easy replaceability. This design encourages users to maintain their phones longer without needing a complete replacement, thus reducing e-waste.",
                "adjective": "durable and replaceable",
                "class_name": "Couldn't find name"
            },
            "durability": {
                "summary": "Fairphone 5 smartphones are built with robust materials and a modular design, promoting repairability and longevity. This durability helps resist physical damage and extends the functional lifespan of the device, reducing the likelihood of early disposal.",
                "adjective": "robust and resilient",
                "class_name": "Couldn't find name"
            },
            "energy_consumption": {
                "summary": "Fairphone 5 devices are designed for energy efficiency, optimizing battery life to extend the time between charges. This focus on energy consumption reduces the overall environmental impact by minimizing energy demands throughout the product's lifecycle.",
                "adjective": "efficient and low-demand",
                "class_name": "Couldn't find name"
            },
            "name": "Use"
        },
        "end_of_life": {
            "planned_obsolescence": {
                "summary": "Fairphone does not engage in planned obsolescence; instead, it promotes longevity through sustainable design and modularity. By avoiding performance-reducing software updates, Fairphone encourages users to keep their devices longer, thereby reducing electronic waste.",
                "adjective": "intentional and sustainable",
                "class_name": "Couldn't find name"
            },
            "second_use": {
                "summary": "Due to its modular design and high-quality construction, the Fairphone 5 is likely to be resold or reused after initial ownership. This encourages a circular economy, reducing waste and extending the life of the device beyond the typical two-year usage period.",
                "adjective": "likely and beneficial",
                "class_name": "Couldn't find name"
            },
            "recycling": {
                "summary": "The components of the Fairphone 5 are designed with recycling in mind, facilitating disassembly and material recovery at the end of their life. Fairphone promotes responsible recycling practices, which help mitigate the demand for raw materials and reduce carbon emissions associated with new material extraction.",
                "adjective": "highly recyclable and proactive",
                "class_name": "Couldn't find name"
            },
            "name": "End of Life"
        },
        "conclusion": {
            "summary": "The Fairphone 5's carbon footprint is influenced by global sourcing, extensive transportation emissions, and production methods. However, its use of over 70% fair or recycled materials, modular design, and energy-efficient features suggest a positive impact, promoting sustainability and longevity while minimizing waste and resource consumption."
        },
        "name": "Fairphone 5"
    }

src = "text_generator"
_ex(resp_dic, src)


"""
