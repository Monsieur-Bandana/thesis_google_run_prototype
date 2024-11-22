from openai import OpenAI
import os
import json

sk = "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"

classes = []
descriptions = []

def classify_text_using_gpt(text, classes, descriptions):
    context = f"""
    I will give you a text and you are about classify it using of the following classes:
    {', '.join([f'- {cls} - {dsr}' for cls in classes for dsr in descriptions])}
    Which class is applicable? It can be multiple or even all. Please avoid assigning labels, if the information about that topic are only minimal. Further provide only the
    explicit label names as a response
    """

    comment = f"""This is the text: "{text}" """
    
    client = OpenAI(api_key=sk)
    
    response = client.chat.completions.create(
        model="gpt-4o",  # Oder ein anderes Modell wie "gpt-4"
        messages=[
            {"role": "system", "content": context},
            {
                "role": "user",
                "content": comment
            }
        ],
        temperature=1  # Geringere Temperatur für deterministischere Ergebnisse
    )
    return response.choices[0].message.content

def extract_classes():
    with open('labels_with_descriptions.json', 'r') as file:
        data: list = json.load(file)

        for el in data:
            classes.append(el["name"])
            descriptions.append(el["description"])

# Beispielaufruf
def exec_file(pdf_text):
    text = pdf_text
    first_20_chars = text[:60]
    if not classes:
        extract_classes()
    print(f"""{first_20_chars} - {classify_text_using_gpt(text, classes, descriptions)}""")

## test section
teststring = f"""

 The European Commission has reinforced its commitment to tackle environmental challenges through the “European Green Deal” (European
 Commission,2019a),whichincludesmeasuresonenergyefficiencyandcirculareconomyperformanceoftheinformationandcommunicationtech
nologies (ICT) sector.
 Thecontribution of the ICTsectortotheglobalGHGemissionswasabout1.4%in2007andcouldexceed14%in2040.Inparticular,thecontri
bution from smartphones is increasing so rapidly that it could soon become greater than desktops, laptops, and displays. The main reasons for this
 growtharethehighmarketpenetrationofsmartphonesandtheirshortreplacementcycles(2yearsonaverage)(Belkhir&Elmeligi,2018).
 In the European Union (EU), ICT products fall within the scope of Ecodesign Directive (European Union, 2009) and Energy Label Regulation
 (EuropeanUnion,2017).Thesesetoutaregulatoryframeworkforimprovingtheenergyefficiencyofenergy-relatedproducts(EuropeanCommis
sion, 2016), with a current shift toward the more systematic consideration of material efficiency aspects (European Commission, 2019b). Material
 efficiency could be defined as the ratio betweentheperformanceofasystemandtheinputofmaterialsrequired(Cordellaetal.,2020a).Asshown
 in Figure 1, material efficiency can be improved along the life cycle of products by strategies that aim to minimize material consumption, waste
 production, and their environmental impacts (Allwood et al., 2011; Huysman et al., 2015). In practice, this could be achieved by designing products
 that aremoredurableandeasiertorepair,reuse,orrecycle(EuropeanCommission,2015).
 The relevance of material efficiency strategies for mitigating climate change impacts depends on the relative impacts associated with each life
 cycle stage of a product (Iraldo et al., 2017; Sanfelix et al., 2019; Tecchio et al., 2016), which can be quantified through life cycle assessment (LCA)
 (ISO, 2006a;ISO,2006b).
 The analysis of LCA studies can provide indications about the environmental impacts of smartphones (Cordella & Hidalgo, 2016). For exam
ple, Andrae (2016), Ercan et al. (2016), and Clément et al. (2020) analyzed the Bill of Materials (BoM) of specific devices and their life cycle GHG


"""

exec_file(teststring)


