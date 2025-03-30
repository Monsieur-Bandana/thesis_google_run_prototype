## Scraper
/scraper (for each brand separate python file) 
## Classifier 
/file_classifier/main.py 
## Interpreter 
/file_interpreter/main.py 
## Text-generator 
/text_generator/main.py 
/shared/llm_after_class.py 
## LLM-Service module 
shared/llm_after_class.py 
## Frontend 
• /frontend/app.py (“main”) 
• /frontend/static/script.js (script file for features) 
• /frontend/static/css/style.css (style sheet) 
* /frontend/templates/index.html (HTML-template)
## Ef-blueprint 
/labels_with_descriptions.json 

## Other information
You will realize, that most of the files contain the variables
"bucket_name"  and "folder_name" or similar
bucket_name sets the folder on the google cloud storage. Here all files referring to thir project are stored.
"folder_name" sets the location where each module saves its files. This was mainly important during development, since all modules are located in the same directory.
