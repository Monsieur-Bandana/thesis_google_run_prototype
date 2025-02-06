from shared.score_calculator.score_analyzer import generate_score

### Materials Section
## test fairphone
resp_str:list[str] = ["""
The Fairphone 5 utilizes metals such as aluminum, copper, cobalt, gold, lithium, and rare earth elements like neodymium and praseodymium. More than 70% of its materials are fair or recycled, including 100% recycled plastics for the back cover, 100% recycled indium in the display, and 100% recycled rare earth elements in the speaker. Fairphone focuses on improving metals sourcing by integrating fairtrade gold and cobalt credits, ensuring ethical practices and reducing environmental impact from mining.
Fairphone 5 components may contain toxic chemicals like lead, mercury, cadmium, and brominated flame retardants, which pose environmental risks during disposal. Fairphone improves by using over 70% fair or recycled materials, integrating fair lithium and cobalt, and ensuring the use of 100% recycled plastics in the back cover, thus enhancing sustainability and reducing harmful impacts.
Natural resources for Fairphone 5 are sourced globally, with cobalt from the Democratic Republic of the Congo, lithium from Chile, and rare earth elements predominantly mined in China. Fairphone focuses on improving Raw Materials Origin by using over 70% fair or recycled materials, ensuring responsible sourcing, and supporting fair labor practices in its supply chain.
""",
"""
The Fairphone 5 involves extensive international shipping, with components traveling from Asia to assembly in Europe, covering approximately 8860 km by air. Fairphone aims to reduce its carbon footprint by using renewable energy in production and ensuring e-waste neutrality, balancing the environmental impact of transportation.
"""
]

## test samsung
resp_str1:list[str]  = ["""
The Galaxy S24 Ultra uses metals such as aluminum, copper, and rare earth elements like neodymium and lithium, essential for components like batteries and magnets. Samsung aims to improve its metals sourcing and reduce environmental impact through responsible mining practices and recycling initiatives. 
Additionally it contains toxic chemicals like PVC, brominated flame retardants (BFRs), and heavy metals such as lead and mercury, which pose environmental risks during production and disposal. Samsung has made efforts to reduce these toxic substances in their smartphones to mitigate pollution and health hazards. 
Natural resources for the Galaxy S24 Ultra are sourced globally, particularly rare earth elements mined in China, the Democratic Republic of the Congo, and Australia. Samsung's improvement efforts focus on adopting renewable energy in manufacturing, optimizing supply chains, and promoting circular economy principles to mitigate environmental impacts.
""",
"""
Samsung smartphones, including the Galaxy S24 Ultra, are produced in Asia and shipped globally, often exceeding thousands of kilometers, contributing to significant carbon emissions. Samsung's logistics operations aim to streamline transportation, but extensive distances remain a challenge.
"""
]

## test iphone
resp_str2:list[str]  = ["""
The iPhone 16 uses metals like aluminum, copper, cobalt, lithium, and rare earth elements such as neodymium and dysprosium. Apple has made significant improvements by incorporating 100% recycled aluminum in the thermal substructure, 100% recycled cobalt and lithium in the battery, and 100% recycled rare earth elements in magnets, along with various other recycled materials in components. 
Additionally it contains toxic chemicals like PVC, brominated flame retardants (BFRs), and heavy metals such as lead. Apple has improved by using 100% recycled materials for various components, eliminating harmful substances like arsenic and mercury, and adhering to strict chemical regulations.
Natural resources for the iPhone 16 primarily come from mines in China, the Democratic Republic of the Congo, and Australia, with significant environmental degradation due to mining practices. Apple has improved Raw Materials Origin by utilizing 100% recycled aluminum, cobalt, lithium, gold, copper, and tin, and aims for over 30% of materials to be recycled by 2030.
""",
"""
pple smartphones, including the iPhone 16, are produced in various locations, primarily in Asia, with components traveling thousands of miles before assembly in China. This extensive transportation network contributes to significant carbon emissions. Apple is working to minimize transportation distances and switch to low-carbon transport methods to reduce its environmental impact.
"""
]

## test redmi
resp_str3:list[str]  = ["""
Xiaomi smartphones, including the Redmi 14C, utilize metals like lithium, cobalt, aluminum, copper, and rare earth elements such as neodymium and dysprosium for batteries and electronic components. The extraction of these metals raises significant environmental concerns due to mining practices. Xiaomi is focused on sourcing these metals responsibly to mitigate environmental degradation. 
As an additional point, the smartphone smartphones contain toxic chemicals such as polyvinyl chloride (PVC), brominated flame retardants (BFRs), and heavy metals like lead and cadmium. These materials pose environmental risks during production and disposal. Xiaomi has not specified any improvement efforts related to reducing toxic chemicals in their devices. 
Natural resources for the Redmi 14C are primarily sourced from mines in China, Australia, and the Democratic Republic of Congo, particularly for rare earth elements. Xiaomi's improvement efforts include optimizing supply chains and adopting renewable energy in production.
""",
"""
The Redmi 14C smartphones are produced in China, with components sourced globally, resulting in transportation distances averaging thousands of kilometers from raw material extraction to assembly and then to retail locations. Xiaomi's transportation-related improvement efforts focus on optimizing logistics to reduce carbon emissions associated with these long-distance travels.
"""
]

test_list = [resp_str, resp_str1, resp_str2, resp_str3]
phone_names = ["fairphone", "samsung", "iphone", "redmi"]
inc_c = 0
for t_ in test_list:
    mat: str =  t_[0]
    transp: str = t_[1]
    if phone_names[inc_c] in "fairphone, iphone":
        print(phone_names[inc_c]+ "-materials: " +str(generate_score(mat, "materials")))
        print(phone_names[inc_c]+ "-transport: " +str(generate_score(transp, "transportation")))
    inc_c = inc_c + 1