import json

def extract_comp_name(dir_):
    main_folder = "shared"

    comps = []
    with open(f"{main_folder}/prefilter.json", "r") as file:
        comps = json.load(file)
    comp = ""
    for li_el in comps:
        if dir_ == li_el["product"]:
            comp = li_el["company"]
    return comp
