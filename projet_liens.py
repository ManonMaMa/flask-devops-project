from flask import Flask, render_template

# Lors du développement d'une app Flask, mettre :
#       les fichiers HTML dans un dossier templates/
#       les fichiers CSS, JS, images dans un dossier static/

# Création de l'application Flask (on indique que ce fichier est le fichier principal).
app = Flask(__name__)       # __name__ : variable spéciale de python contenant le nom de ce fichier.

@app.route("/")     # Définition de la route principale : http://127.0.0.1:5050/
def index():
    """Retourne le fichier index.html du dossier templates/ grâce à la fonction render_template() de Flask."""
    return render_template('index.html')

@app.route("/")     # Définition de la route principale : http://127.0.0.1:5050/
def index():
    """Retourne le fichier index.html du dossier templates/ grâce à la fonction render_template() de Flask."""
    return render_template('index.html')

@app.route("/videos")
def affiche_videos():
    return render_template('videos.html')

@app.route("/videos/search")
def search():
    return render_template('search.html')

@app.route("/videos/add")
def add():
    return render_template('add.html')

@app.route("/videos/<int:id>")
def video():
    return id


# Lancement du serveur : mode debug et hot reload actif.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

