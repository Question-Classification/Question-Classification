# Prepared vs. spontaneous question classification

This repository contains the work (being) done by students of Paris Nanterre University's NLP Masters Degree for the task of prepared vs. spontaneous question classification.

Install the required dependencies from the ```requirements.txt``` file in a ".venv" virtual environment. 

## **Programs :**
---

### **Cleaning and alignment programs :**
* ```clean_repo.py``` : used to clean the repository because of the large amount of useless files
* ```clean_acsynt.py``` : (not used)
* ```prepare_manual_annotation_acsynt.py``` : (not used)
* ```alignement.py``` : try to align all ESLO files (not used)
* ```prepare_manual_annotation.py``` : (not used) try to create a new column in all_questions_to_keep.csv containing the name of the file corresponding to each question
* ```trs_to_tg.pl``` : (used to prepare manual annotation) the program used to convert from Transcriber Transcript (.trs) to Praat TextGrid (.TextGrid)
* ```tg_alignment.py``` : (used to prepare manual annotation) the program used to prepare manual annotation for ESLO corpora, it calls ```trs_to_tg.pl``` when aligning the ESLO corpora
* ```merge_tg.py``` : (used to create hybrid TextGrid files for the ACSYNT corpora, with Webmaus + EasyAlign TextGrids) used to create exploitable ACSYNT TextGrid files

### **Prepare data for features extraction :**
These programs were used to transform a TextGrid file with multiple tiers to a TextGrid file with only a single tier
* ```reformat_2tiersFile_to1tier.py```  
* ```reformat_3tiersFile_to1tier.py```  
* ```reformat_4tiersFile_to1tier.py``` 
* ```reformat_5tiersFile_to1tier.py``` 
### **Extraction program :**
* ```extraction_features.py``` : the program used to extract prosodic features
### **Normalize values :**
* ```normalize.py``` : used to normalize "mean_syll_duration (ms)" and "mean_syll_duration_last_3_syll (ms)" values
### **Dataset exploration :**
* ```stats.py```: used to compute stats (number of questions, means for each feature, etc.) for the entire final corpora (ESLO + ACSYNT)
