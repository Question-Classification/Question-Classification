import pandas as pd
from pathlib import Path
import re
import bs4 as bs
from unidecode import unidecode
from tqdm import tqdm

tqdm.pandas()

# but du code : préparer l'annotation manuelle pour pouvoir trouver les
# questions à réaligner sous praat par la suite
# le pb est que les temps qu'on a correspondent à l'intégralité du tour
# et pas uniquement aux questions qui sont dans ce tour de parole


ROOT_DATA_DIR = "../data/"

# ça ne va marcher que pour les questions eslo (acsynt pas la même manière de parser)
def retrieve_file_information(row):
    # on récupère les data du fichiers des anciens étudiants et on nettoie

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

    # go through all trs files in ESLO
    directory = ROOT_DATA_DIR+"ESLO/"
    pathlist = Path(directory).rglob("*.trs")
    for trs_path in pathlist:
        trs_path = re.sub(r"\\", "/", str(trs_path))
        # chargement du fichier XML et création de l'object qui est le document parsé
        source = open(trs_path, encoding="utf-8").read()
        soup = bs.BeautifulSoup(source, "xml")
        # on cherche tous les "Turn" dans le XML pour avoir la longueur des tours de parole à traiter
        all_turns = soup.findAll("Turn")
        for i in range(len(all_turns) - 5):
            # on récupère le texte de ce tour de parole et les contextes dans les trs, nettoyage
            text = all_turns[i].getText()
            left_list = all_turns[max(0, i - 5) : i]
            left_text_list = []
            right_text_list = []
            for elt_left in left_list:
                left_text_to_add = elt_left.getText()
                clean_left_text_to_add = re.sub(r"\n+", " ", left_text_to_add)
                clean_right_text_to_add = clean_left_text_to_add.strip(r"\s")
                left_text_list.append(clean_left_text_to_add)

            right_list = all_turns[i + 1 : i + 6]
            for elt_right in right_list:
                right_text_to_add = elt_right.getText()
                clean_right_text_to_add = re.sub(
                    r"\n+", " ", right_text_to_add
                )
                clean_right_text_to_add = clean_right_text_to_add.strip(r"\s")
                right_text_list.append(clean_right_text_to_add)

            clean_text = re.sub(r"\n+", " ", text)

            # print(
            #     "left_question",
            #     clean_left_question_to_keep,
            #     "question",
            #     clean_question_to_keep,
            #     "right question",
            #     clean_right_question_to_keep,
            #     "*****",
            #     "left",
            #     "|".join(left_text_list),
            #     "text",
            #     clean_text,
            #     "right",
            #     "|".join(right_text_list),
            #     "file :",
            #     trs_path,
            #     end="$$$$$$$$$\n",
            # )

            # récupération et nettoyage contextes dans les fichiers trs
            left_context = "|".join(left_text_list)
            clean_left_context = re.sub(r"\s+", " ", left_context)
            right_context = "|".join(right_text_list)
            clean_right_context = re.sub(r"\s+", " ", right_context)

            # se baser uniquement sur la colonne question
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
                            trs_path,
                            "left question",
                            clean_left_question_to_keep,
                            "question",
                            clean_question_to_keep,
                            "right question",
                            clean_right_question_to_keep,
                            "*****",
                            "trs contexte gauche",
                            clean_left_context,
                            "trs question",
                            clean_text,
                            "trs contexte droit",
                            clean_right_context,
                        )

                        return trs_path

def main():
    df = pd.read_excel(
        ROOT_DATA_DIR+"all_questions_to_keep.xlsx",
    )

    df["file_name"] = df.progress_apply(
        lambda row: retrieve_file_information(row), axis=1
    )

    df.to_csv(ROOT_DATA_DIR+"all_questions_to_keep_filenames.csv", sep=";", encoding="utf-8")

if __name__ == "__main__":
    main()