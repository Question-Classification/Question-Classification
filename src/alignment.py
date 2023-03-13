import parselmouth
import glob
import os.path
import bs4 as bs
import tgt
import re 


def cleaning(text):
    """This function cleans the text to remove line breaks."""
    cleaned_text = re.sub("\n", " ", text)
    return cleaned_text


def align_one_ESLO_file():
    """This functions allows the alignement of one ESLO type file."""
    # chargement du fichier XML et création de l'object qui est le document parsé 
    source = open("data/ESLO2_CINE_1176_C.trs", encoding="utf-8").read()
    soup = bs.BeautifulSoup(source, 'xml')

    # ouverture du fichier son avec parselmouth
    sound = parselmouth.Sound("data/ESLO2_CINE_1176.wav")

    # creation du textgrid à partir du fichier son avec une tier intervalle "turns"
    grid = parselmouth.praat.call(sound, "To TextGrid", "turns", "")
    # la grille devient un objet tgt > manipulable avec ses propres méthodes
    grid = grid.to_tgt()

    print(type(grid))

    # on récupère la tier précédemment créée
    interval_tier = grid.get_tier_by_name("turns")

    # on cherche tous les "Turn" dans le XML pour avoir la longueur des tours de parole à traiter
    all_turns = soup.findAll('Turn')

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
        interval = tgt.core.Interval(float(start_time),float(end_time),cleaning(text))
        # on ajoute l'intervalle à la tier (IntervalTier)
        interval_tier.add_interval(interval)
        # grille.tgt.io.export_to_long_textgrid(grille)

    # on exporte le résultat sous forme de long textgrid (on a aussi un format court)
    export = tgt.io.export_to_long_textgrid(grid)
    print(export)

    # on sauvegarde l'export qui est une simple string dans un fichier .TextGrid
    with open("data/test_grille.TextGrid", "w", encoding="utf-8") as out :
        out.write(export)


def main():
    align_one_ESLO_file()


if __name__ == "__main__":
    main()