from transformers import AutoModelForCausalLM, AutoTokenizer

def accessScientificInformation() -> str:
    return f"""Key Emission Sources in the Smartphone Lifecycle
Material Extraction and Manufacturing: These stages are the highest contributors to CO2 emissions, largely due to the energy-intensive processes of mining and refining materials, like cobalt, copper, gold, and silver. The printed wiring board (PWB), integrated circuits (ICs), and display assembly collectively contribute 75% of material-related emissions.

Assembly, Distribution, and Usage:

Assembly: Emissions during the assembly phase account for around 16% of the total CF, with high energy use during manufacturing.
Distribution: Emissions occur primarily due to global transportation (e.g., air freight from production sites).
Usage: Recharging and, notably, the energy required for mobile communication services significantly increase emissions. The latter, which includes network and data center operations, can double or even triple the CF, especially with increased data usage (e.g., streaming).
End-of-Life (EoL) Scenarios: While recycling reduces emissions by enabling the recovery of valuable materials, only a partial recovery is economically viable, limiting its overall impact.

Strategies for Reducing Carbon Emissions
Extending Product Lifespan:

Longer Replacement Cycles: Extending the replacement cycle from two years to three or four significantly reduces the CF by 30-44%, as fewer units are required over a given period.
Repair and Refurbishment: Repairing components, such as batteries and displays, can extend device life without the need for new manufacturing. Battery replacement, for instance, allows a three-year replacement cycle, reducing emissions by approximately 30%.
Use of Secondary Markets:

Remanufactured and Second-Hand Devices: Replacing new purchases with remanufactured or second-hand phones can cut the CF by up to 80% under optimal conditions. The CF reduction varies depending on whether the phone is fully refurbished (about 50%) or lightly refurbished.
Lean and Durable Design:

Material Efficiency: Designs that reduce material quantities by up to 30% can lower emissions by 7%. However, trade-offs are necessary, as durable designs may make repairs more challenging.
Modular Design: Facilitates easy disassembly and repair, helping prolong device life. Enhanced durability for components most prone to damage, like displays and batteries, also aids in reducing emissions over time.
End-of-Life Recycling:

Efficient Recycling Processes: Improved recycling of metals and critical components could cut emissions further by up to 30%. However, actual benefits depend on effective collection and recycling rates, which are currently low."""

# Eingabetext
def generateAnswer(input: str, model, tokenizer)  -> str:
    
    model = model
    tokenizer = tokenizer
    context = accessScientificInformation()
    comment = f"""please tell me about the carbon footprint of the {input}"""
    prompt_template_w_context =  lambda context, comment: f"""[INST]please tell me about the carbon footprint of the {comment}
    
    use the following text as a source of validation:
    {context}
    /[INST]"""

    prompt = prompt_template_w_context(context, comment)

    # Tokenisierung des Eingabetexts
    inputs = tokenizer(prompt, return_tensors="pt")

    # Modell generiert Vorhersagen
    outputs = model.generate(inputs["input_ids"], max_length=1000, num_return_sequences=1)

    # Generierten Text dekodieren
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(generated_text)

    return generated_text
