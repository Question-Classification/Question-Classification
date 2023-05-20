import pandas as pd
import re

ROOT_DATA_DIR = "../data/"
FILENAME = "all_questions_to_keep_cleaned.xlsx"

df = pd.read_excel(ROOT_DATA_DIR+FILENAME)

annotated = df[df['fichier'].notna()]

prepared = annotated[annotated['categorie'] == "préparé"]
spontaneous = annotated[annotated['categorie'] == "spontané"]
non_question = annotated[annotated['categorie'] == "non-question"]

print("Nombre total de questions annotées :", len(annotated))
print("Nombre de questions préparées :", len(prepared))
print("Nombre de questions spontantées :", len(spontaneous))
print("Nombre de non questions :", len(non_question))

regex = re.compile(r"#?spk\d(\s: )?")

cleaned_questions = annotated["question"].apply(lambda row: re.sub(regex, "", row.strip()))
unique = set(cleaned_questions.to_list())

print("Nombre de questions uniques :", len(unique))