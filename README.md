# Question-Classification

Install the required dependencies from the ```requirements.txt``` file in a ".venv" virtual environment. 

## The corpus to be aligned : 

* ESLO ([link](https://www.ortolang.fr/market/corpora/eslo/?path=%2F)) :
  - [x] ESLO 1 ENTRETIEN (ENT)
  - [x] ESLO 1 INTERVIEW (INTPERS)
  - [x] ESLO 2 CINE
  - [x] ESLO 2 REPAS
 
* ACSYNT ([link](https://www.ortolang.fr/market/corpora/sldr000832?path=%2F)): 
  - [x] Entretiens guidés 


## Programs :
* clean_repo.py : used to clean the repository because of the large amount of useless files
* alignement.py : used to align all ESLO files
* prepare_manual_annotation.py : used to create a new column containing the name of the file corresponding to each question