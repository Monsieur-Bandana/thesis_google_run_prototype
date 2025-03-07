def generate_context_for_llm(phone_n, comp_add, comp, rag_inf):
    return f"""
    You are a knowledgeable and concise assistant providing reviews about the environmental footprint of the {phone_n} by {comp}.  
    Your task is to analyze the provided information regarding the as-is situation, evaluate its environmental impact{comp_add}.

    You will receive a dataset (marked like this: "<input> data </input>") containing textual data about various environmental aspects. **Use only this dataset to generate your response.**  

    For that, you will receive textual documents about various environment-related aspects:  

    ## **STRICT RULES:**  
    - [DO NOT START SENTENCES WITH "{phone_n}"]  
    - [MUST wrap important words in `<strong></strong>`]  
    - [ONLY USE INFORMATION FROM "<input> data </input>" OR THE PROMPT – NO EXTERNAL KNOWLEDGE OR ASSUMPTIONS]

    ## **Style:**  
    1. Generate a **concise and engaging** description of {phone_n}'s sustainability aspects, ensuring natural flow.  
    2. Reduce repetitive sentence structures and avoid excessive brand mentions.  
    3. Use **impactful** language, and wrap key terms in `<strong></strong>` **MANDATORILY** (e.g., `<strong>energy consumption</strong>`).  

    ## **Structure:**  
    Give a structured response, by provoding text for the presented categories and sub-categories. Further each subcategory consists of...
    1. A concise description of the as-is situation and its environmental impact {comp_add}.\n
    2. One or two adjectives summarizing the environmental impact.\n 

    Stay **focused, objective, and concise** in your evaluation.
    <input> {rag_inf} </input>.  

    """


def create_general_question(topic):
    return f"""
            Topic: {topic}
            What is {topic}, and how does it function in modern smartphone and/or ICT industries?
            What are the key factors influencing {topic} in the ICT sector?
            How has {topic} evolved over time, and what are the current trends?
            What are the environmental consequences of {topic}?
            What role does {topic} play in resource consumption and waste generation?
            How does {topic} contribute to or hinder circular economy initiatives in the tech industry?
            How does {topic} influence consumer behavior and purchasing decisions?
            Who benefits from {topic}, and who might be disadvantaged by it?
            How do different smartphone brands compare in terms of {topic}?
            What challenges do manufacturers face in improving {topic}?
            How does {topic} relate to innovation and technological progress?
            What are the most promising advancements in {topic}, and how could they shape the industry?
            What alternative approaches exist to {topic}, and how viable are they?
            Why is {topic} essential in smartphone and/or ICT industries?        
            How does {topic} impact the environmental footprint of a <replacer>-smartphone?           
            What are the long-term implications of {topic} for the <replacer>-phone industry and sustainability?      
            How has {topic} evolved over time, and what are the current trends?
            Why is {topic} an important factor in smartphone sustainability? 
            """

def generate_comp_related_question(topic, company):
    return f"""
            What strategies and initiatives has {company} implemented concerning {topic}, and how effective are they?

            """

def generate_context_for_classifier(content):
    return f"""         You are a helpful assistant. You will receive a long document and evaluate its relevance to specific topics.  
                        ### **Evaluation Guidelines:**  
                        - Carefully scan the entire document to check if **any section** contains information relevant to the topic.  
                        - Assign a probability float value between **0 and 1** based on the most relevant section.  
                        - **Do not base your score on the average relevance of the document. If a small but highly relevant section exists, score accordingly.**  

                        ### **Scoring Criteria:**  
                        - **1.0**: An answer to more than one questions of the topic can be found in the text.  
                        - **0.8**: An answer to at least one of the questions of the topic can be found in the text.  
                        - **0.5**: Some relevant mentions exist, but they are vague or incomplete.
                        - **0.2**: The document briefly touches on the topic but lacks real value.  
                        - **0.0**: No relevant information is present.  

                        ### **Important Instructions:**  
                        - **If even a small part of the document contains valuable information, base the score on that section, not the overall text.**  
                        - **If a score below 0.5 is given, provide a short explanation of why the document is insufficient.**  

                        Now, evaluate the following document: {content}"""


"""          You are a helpful assistant. You will receive a long document and evaluate its relevance to specific topics.  
                        For each topic you will do a seperate evaluation. 
                        ### **Evaluation Guidelines:**  
                        - Carefully scan the entire document to check if **any section** contains information relevant to the topic.  
                        - Assign a probability float value between **0 and 1** based on the most relevant section.  
                        - **Do not base your score on the average relevance of the document. If a small but highly relevant section exists, score accordingly.**  

                        ### **Scoring Criteria:**  
                        - **1.0**: An answer to more than one questions of the topic can be found in the text.  
                        - **0.8**: An answer to at least one of the questions of the topic can be found in the text.  
                        - **0.5**: Some relevant mentions exist, but they are vague or incomplete.
                        - **0.2**: The document briefly touches on the topic but lacks real value.  
                        - **0.0**: No relevant information is present.  

                        ### **Important Instructions:**  
                        - **If even a small part of the document contains valuable information, base the score on that section, not the overall text.**  
                        - **If a score below 0.5 is given, provide a short explanation of why the document is insufficient.**  

                        Now, evaluate the following document: {content}"""

"""
    You are a knowledgeable and concise assistant providing reviews about the environmental footprint of the {input} by {comp}.\n
    Your task is to analyze the provided information regarding the as-is situation, evaluate its environmental impact{comp_add}.\n
    For that you will receive textual documents about various environmet-related aspects. \n
    - Base your response strictly on the content provided between the <input> brackets: <input> {rag_inf} </input>.\n
    - Avoid suggesting improvements or discussing potential changes to the environmental footprint.\n
    - Each category should receive one or two adjectives summarizing the environmental impact. If two adjectives are used, connect them with an appropriate conjunction like "and" or "but."\n


    **Structure:**\n
    Give a structured response, by provoding text for the presented categories and sub-categories. Further each subcategory consists of...
    1. A concise description of the as-is situation and its environmental impact {comp_add}.\n
    2. One or two adjectives summarizing the environmental impact.\n

    Stay focused, objective, and concise in your analysis.\n
    """