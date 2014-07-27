math-addressbook
================
Ce petit script permet de générer une grande partie du carnet d'adresse du de l'Association des étudiants en Mathématique et Satistique de l'Université Laval. Il suffit de fournir l'ensemble des données du carnet d'adresse dans un format csv (que l'on peut construire facilement avec un formulaire google docs par exemple) au script et celui-ci va former le code latex nécessaire au gabarit.

Le script est dans le dossier python, le gabarit latex est dans le dossier latex et un exemple complet est donné dans le dossier data.

Voilà comment exécuter le programme:
```batch
addressbook.py /path/to/data.csv /path/to/output/directory/
```