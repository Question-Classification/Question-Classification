from pathlib import Path
import parselmouth
import glob
import os.path
import bs4 as bs
import tgt
import re
# tester sur fichier INTPERS 401


def cleaning(text):
    """This function cleans the text to remove line breaks."""
    cleaned_text = re.sub("\n", " ", text)
    return cleaned_text


def align_one_ESLO_file(wav_path, trs_path, file_name):
    """This functions allows the alignment of one ESLO type file."""
    # remplacer les "\" par "/" pour les chemins
    trs_path = re.sub(r"\\", "/", trs_path)
    wav_path = re.sub(r"\\", "/", wav_path)
    # chargement du fichier XML et création de l'object qui est le document parsé
    source = open(trs_path, encoding="utf-8").read()
    soup = bs.BeautifulSoup(source, "xml")

    # ouverture du fichier son avec parselmouth
    sound = parselmouth.Sound(wav_path)

    # creation du textgrid à partir du fichier son avec une tier intervalle "turns"
    grid = parselmouth.praat.call(sound, "To TextGrid", "turns", "")
    # la grille devient un objet tgt > manipulable avec ses propres méthodes (Read, write, and manipulate Praat TextGrid files with Python)
    grid = grid.to_tgt()

    print(type(grid))

    # on récupère la tier précédemment créée
    interval_tier = grid.get_tier_by_name("turns")

    # on cherche tous les "Turn" dans le XML pour avoir la longueur des tours de parole à traiter
    all_turns = soup.findAll("Turn")

    # pour chaque tour de parole dans le XML
    for i in range(len(all_turns)):
        # on récupère le texte de ce tour de parole
        text = all_turns[i].getText()
        print(text)
        # on récupère la valeur de l'attribut startTime
        start_time = all_turns[i].attrs["startTime"]
        print("Start time : ", start_time, type(start_time))
        # on récupère la valeur de l'attribut endTime
        end_time = all_turns[i].attrs["endTime"]
        print("End time :", end_time, type(end_time))

        # création d'un intervalle pour chaque tour avec le tps de début, fin et le texte nettoyé
        interval = tgt.core.Interval(
            float(start_time), float(end_time), cleaning(text)
        )
        # on ajoute l'intervalle à la tier (IntervalTier)
        interval_tier.add_interval(interval)
        # grille.tgt.io.export_to_long_textgrid(grille)

    # on exporte le résultat sous forme de long textgrid (on a aussi un format court)
    export = tgt.io.export_to_long_textgrid(grid)
    print(export)

    # on sauvegarde l'export qui est une simple string dans un fichier .TextGrid
    save_name = file_name + ".TextGrid"
    with open(save_name, "w", encoding="utf-8") as out:
        out.write(export)


def align_all_ESLO_files():
    directory = "data/ESLO/"
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
    main()
