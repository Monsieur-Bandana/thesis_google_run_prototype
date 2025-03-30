# Scraper 
/scraper
# Classifier 
/file_classifier/main_ai_driven.py 
# Interpreter 
/file_interpreter/main_structured_single.py 
# Text-generator 
/text_generator/main.py 
# LLM-Service module 
• /shared/llm_after_class.py (“main”) 
• /shared/structured_output_creator.py (for structured output) 
# Scoring module 
• /shared/score_calculator/score_analyzer.py (API calls and total score calculator) 
• /shared/score_calculator/score_examples.json (few shots) 
# Frontend 
• /frontend/app.py (“main”) 
• /frontend/html_generator.py (transforms dictionaries into HTML) 
• /frontend/static/script.js (script file for features) 
• /frontend/static/css/style.css (style sheet) 
• /frontend/templates/index.html (html template) 
# EF-blueprint 
/main/labels_with_descriptions_structured.json 
# Question-collection
/shared/question_builder.py 
# Further notes
You will realize, that most of the files contain the variables
"bucket_name"  and "folder_name" or similar
bucket_name sets the folder on the google cloud storage. Here all files referring to thir project are stored.
"folder_name" sets the location where each module saves its files. This was mainly important during development, since all modules are located in the same directory.
