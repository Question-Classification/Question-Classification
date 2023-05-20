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
* ```tg_alignment.py``` : (used to prepare manual annotation) the program used to prepare manual annotation

### **Prepare data for features extraction :**
All this programs were used to transform a TextGrid file with n tiers to a TextGrid file with only a single tier
* ```reformat_2tiersFile_to1tier.py```  
* ```reformat_3tiersFile_to1tier.py```  
* ```reformat_4tiersFile_to1tier.py``` 
* ```reformat_5tiersFile_to1tier.py```
### **Extraction program :**
* ```extraction_features.py``` : the program used to extract prosodic features

