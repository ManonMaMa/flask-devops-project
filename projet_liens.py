import json
from flask import Flask, request, render_template

# Lors du développement d'une app Flask, mettre :
#       les fichiers HTML dans un dossier templates/
#       les fichiers CSS, JS, images dans un dossier static/

# Création de l'application Flask (on indique que ce fichier est le fichier principal).
app = Flask(__name__)       # __name__ : variable spéciale de python contenant le nom de ce fichier.

@app.route("/")     # Définition de la route principale : http://127.0.0.1:5050/
def index():
    """Retourne le fichier index.html du dossier templates/ grâce à la fonction render_template() de Flask."""
    return render_template('index.html')

@app.route("/videos")
def affiche_videos():
    with open("./videos.json", "r", encoding="utf-8") as f:
        videos = json.load(f)
    return render_template("videos.html", videos=videos)

@app.route("/videos/search")
def search():
    # Rechercher des vidéos par titre  
    # Affiche un formulaire de recherche et les résultats de recherche. 

    return render_template('search.html')

@app.route("/videos/add")
def add():
    if request.method == 'POST':
        # route qui permet d'ajouter une nouvelle vidéo à la playlist

        return render_template('add.html')
    if request.method == 'GET':
        # Affiche le formulaire pour ajouter une nouvelle video. 

        return render_template('add.html')

@app.route("/videos/<int:id>")
def video(id):
    return render_template('details_video.html')


# Lancement du serveur : mode debug et hot reload actif.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

