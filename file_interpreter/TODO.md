donwload and read json from google cloud storage
the json file includes entities containg a class name, class description and related terms

download and read json2 from google cloud storage
json2 includes entities containg the name of a pdf and a list of classes fitting to the pdf

for class 
select all fitting pdfs containing class
load those pdfs from google cloud storage
ask gpt api to summarize each pdf with focus on the class and related terms
add each summery to txt file. give text file the name of the class