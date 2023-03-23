from pathlib import Path
import os


def main():
    """This function's aim is to clean the repo where we only need .trs .wav
    and .TextGrid newly created files"""
    directory = "data/"
    pathlist = Path(directory).rglob("*")
    for path in pathlist:
        if str(path).endswith("22km.wav"):
            os.remove(path)
            print("22km removed")
        elif str(path).endswith(".meta.xml"):
            os.remove(path)
            print("meta XML removed")
        elif str(path).endswith(".mp3"):
            os.remove(path)
            print("mp3 removed")
        elif str(path).endswith(".tei_corpo.xml"):
            os.remove(path)
            print("tei corpo removed")


if __name__ == "__main__":
    main()
