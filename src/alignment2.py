from pathlib import Path
import parselmouth
import glob
import os.path
import bs4 as bs
import tgt
import re
import pandas as pd


    

# Faut voir si le nettoyage est bon, plutôt remplacer les retours à la ligne par "//"
# Mais il existe des cas où les retours à la ligne ne sont pas traîtés (ils ont été gardés, sans traitement), ce point on peut vérifier avec Angèle pour savoir 
def cleaning(text):
    """This function cleans the text to remove line breaks."""
    cleaned_text = re.sub("\n", " ", text)
    # add this condition to keep only questions
    if "?" in cleaned_text:
        segment_list = cleaned_text.split("  ")
        for segment in segment_list:
            if "?" in segment:
                # cleaned_text = "#" + spk + " : " + segment
                cleaned_text = segment
    return cleaned_text

# df = pd.read_csv("data/all_questions.csv")
df = pd.read_excel("data/all_questions_new.xlsx")

# process "text" column and save the result in the column "processed_text"
df.insert(df.columns.get_loc('question') + 1, 'processed_question', df['question'].apply(lambda x: cleaning(x)))



def get_label1(text):
    if "?" in text:
        text = text.split("  ")
        for segment in text:
            if "?" in segment:
                label = "type de question"
    else:
        label = ""
    return label


def get_label(text: str):
    """This function allows to get question labels: spontané, préparé ou non-question and add them to TextGrid file."""
    if "?" in text:
        text = text.split("  ")
        for segment in text:   
            if "?" in segment:
                condition = df.processed_question == segment
                if condition.any():
                    label = df[condition].categorie.values[0]
                else:
                    label = "type de question non-trouvé"
    else:
        label = ""
    return label

def align_one_ESLO_file(wav_path, trs_path, file_name):
    """This function allows the alignment of one ESLO type file."""
    # remplacer les "\" par "/" pour les chemins
    trs_path = re.sub(r"\\", "/", trs_path)
    wav_path = re.sub(r"\\", "/", wav_path)
    # chargement du fichier XML et création de l'object qui est le document parsé
    source = open(trs_path, encoding="utf-8").read()
    soup = bs.BeautifulSoup(source, "xml")

    # ouverture du fichier son avec parselmouth
    sound = parselmouth.Sound(wav_path)
# ---------------------------------------------
    # création d'un objet TextGRid
    textgrid = tgt.core.TextGrid()
    # Création de deux objets Tier
    interval_tier = tgt.core.IntervalTier(name="turn", start_time=sound.xmin, end_time=sound.xmax)
    interval_tier_labels = tgt.core.IntervalTier(name="labels", start_time=sound.xmin, end_time=sound.xmax)
# ---------------------------------------------


    # on cherche tous les "Turn" dans le XML pour avoir la longueur des tours de parole à traiter
    all_turns = soup.findAll("Turn")

    # pour chaque tour de parole dans le XML
    for i in range(len(all_turns)):
        # on récupère le texte de ce tour de parole
        text = all_turns[i].getText()
        print(text)
        # on récupère les speakers
        # spk = all_turns[i].attrs["speaker"]
        # print("spk : ", spk, type(spk))
        # on récupère la valeur de l'attribut startTime
        start_time = all_turns[i].attrs["startTime"]
        print("Start time : ", start_time, type(start_time))
        # on récupère la valeur de l'attribut endTime
        end_time = all_turns[i].attrs["endTime"]
        print("End time :", end_time, type(end_time))

        # création d'un intervalle pour chaque tour avec le tps de début, fin et le texte nettoyé
        cleaned_text = cleaning(text)
        interval = tgt.core.Interval(
            float(start_time), float(end_time), cleaned_text
        )
        interval_labels = tgt.core.Interval(
            float(start_time), float(end_time), get_label(cleaned_text)
        )
        # on ajoute l'intervalle à la tier (IntervalTier)
        interval_tier.add_interval(interval)
        interval_tier_labels.add_interval(interval_labels)
        # grille.tgt.io.export_to_long_textgrid(grille)

    # on ajoute les deux objets Tier à l'objet TextGrid
    textgrid.add_tier(interval_tier)
    textgrid.add_tier(interval_tier_labels)

    # on exporte le résultat sous forme de long textgrid (on a aussi un format court)
    export = tgt.io.export_to_long_textgrid(textgrid)
    print(export)

    # on sauvegarde l'export qui est une simple string dans un fichier .TextGrid
    save_name = file_name + ".TextGrid"
    with open(save_name, "w", encoding="utf-8") as out:
        out.write(export)


def align_all_ESLO_files():
    directory = "data/"
    pathlist = Path(directory).rglob("*.wav")
    for wav_path in pathlist:
        if not str(wav_path).endswith("22km.wav"):
            file_name = re.sub(".wav", "", str(wav_path))
            trs_path = file_name + "_C.trs"
            print(wav_path, "////", trs_path)
            align_one_ESLO_file(str(wav_path), trs_path, file_name)


def main():
    # align_one_ESLO_file()
    align_all_ESLO_files()


if __name__ == "__main__":
    # all_questions = df.question.to_list()
    # all_raw_question = [question.split(" : ")[-1] for question in all_questions]
    # print(all_raw_question)
        
    main()
