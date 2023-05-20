import pandas as pd
from pathlib import Path
import re
import os
from tqdm import tqdm
import codecs
from unidecode import unidecode

tqdm.pandas()

ROOT_DATA_DIR = "data/"

def interpret_iso(txt_path):

	# suppression fichiers iso 
	directory = ROOT_DATA_DIR+"ACSYNT/"
	pathlist = Path(directory).rglob("*-iso.txt")
	for iso_path in pathlist: 
		os.system(f'rm -f {iso_path}')

	stem = Path(re.split("/", txt_path)[-1]).stem
	path_list = re.split(r'\\', txt_path)[:-1]
	path = '\\'.join(path_list)+"\\"
	iso_path = path+stem+"-iso.txt"()

	print("stem", stem, "path", path, "txt path", txt_path)

	with codecs.open(txt_path, "r", encoding="ISO-8859-1") as source:
		if not os.path.exists(iso_path):
			with codecs.open(path+stem+"-iso.txt", "w", "ISO-8859-1") as target:
				contents = source.read().encode("ISO-8859-1").decode("ISO-8859-1")
				target.write(contents) 
				with open(path+stem+"-iso.txt", "r", encoding="utf-8") as utf8_input :
					print(utf8_input.read())
					return utf8_input.read()

def retrieve_file_information(row):
	question_to_keep = row["question"]
	left_question_to_keep = row["previous_5_turn"]
	right_question_to_keep = row["next_5_turn"]

	regex = re.compile(r"#?spk\d(\s: )?")

	clean_question_to_keep = re.sub(regex, "", question_to_keep)
	clean_question_to_keep.strip(r"\s+")
	clean_left_question_to_keep = re.sub(
		regex, "", str(left_question_to_keep)
	)
	clean_left_question_to_keep = re.sub(
		r"\s+", " ", clean_left_question_to_keep
	)
	clean_right_question_to_keep = re.sub(
		regex, "", right_question_to_keep
	)
	clean_right_question_to_keep = re.sub(
		r"\s+", " ", clean_right_question_to_keep
	)

	directory = ROOT_DATA_DIR+"ACSYNT/"
	pathlist = Path(directory).rglob("*.txt")
	for txt_path in pathlist:
		source = interpret_iso(str(txt_path)).split("\n") # permet de lire le fichier à partir de l'encodage latin 1
		print(source)
		for i in range(len(source) - 5):
			text = source[i].lower()
			left_list = source[max(0, i - 5) : i]

			left_text_list = []
			right_text_list = []
			for elt_left in left_list:
				clean_left_text_to_add = re.sub(r"\n+", " ", elt_left)
				clean_right_text_to_add = clean_left_text_to_add.strip(r"\s")
				left_text_list.append(clean_left_text_to_add)

			right_list = source[i + 1 : i + 6]
			for elt_right in right_list:
				clean_right_text_to_add = re.sub(
                    r"\n+", " ", elt_right
                )
				clean_right_text_to_add = clean_right_text_to_add.strip(r"\s")
				right_text_list.append(clean_right_text_to_add)

			clean_text = re.sub(r"\n+", " ", text)

			left_context = "|".join(left_text_list)
			clean_left_context = re.sub(r"\s+", " ", left_context)
			right_context = "|".join(right_text_list)
			clean_right_context = re.sub(r"\s+", " ", right_context)

			print("question etudiants :", clean_question_to_keep, "question fichiers", clean_text)
			if re.match(unidecode(clean_question_to_keep), unidecode(clean_text)):
				print("--- même question trouvée")

				# se baser sur les 5 tours avant*
				if re.search(unidecode(clean_left_question_to_keep), unidecode(clean_left_context)):
					print("--- même question et même contexte gauche ")

					# se baser sur les 5 tours après
					if re.search(
						unidecode(clean_right_question_to_keep), unidecode(clean_right_context)
					):

						print(
							"--- même question, même contexte gauche et même contexte droit\n -------- OK -- file found",
							txt_path,
							"left question",
							clean_left_question_to_keep,
							"question",
							clean_question_to_keep,
							"right question",
							clean_right_question_to_keep,
							"*****",
							"txt contexte gauche",
							clean_left_context,
							"txt question",
							clean_text,
							"txt contexte droit",
							clean_right_context,
						)

						return txt_path


def main():

	df = pd.read_excel(
		ROOT_DATA_DIR+"all_questions_to_keep.xlsx",
	)

	df["file_name"] = df.progress_apply(
		lambda row: retrieve_file_information(row), axis=1
	)

	df.to_csv(ROOT_DATA_DIR+"all_questions_to_keep_filenames_acsynt.csv", sep=";", encoding="utf-8")

if __name__ == '__main__':
	main()

