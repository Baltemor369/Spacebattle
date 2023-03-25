from modules.MangaUI import UI
import os

# build executable : pyinstaller --name MangaManager --noconsole --onefile --add-data "asset/*:asset" --path asset modules main.py

# To do :
# + refaire affichage statistique
# + développer module historique(moyenne par semaine/mois voir combien ont été ajout pendant une semaine donnée)
# + multiple delete && button "undo"
# + proposer une couleur de fonds par nom de manga
# + rendre la réécriture plus optimisée

# if folder doesn't exist, create it
if not os.path.exists("data"):
    os.mkdir("data")

# if file doesn't exist, create it
if not os.path.exists("data/backup.txt"):
    os.system("type nul > data/backup.txt")

# if file doesn't exist, create it
if not os.path.exists("data/data.txt"):
    os.system("type nul > data/data.txt")

ui = UI()
ui.mainloop()