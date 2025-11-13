import json, re, os
from flask import Flask, request, render_template, redirect


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

@app.route("/videos/search", methods=["GET","POST"])
def search():
    # Rechercher des vidéos par titre  
    # Affiche un formulaire de recherche et les résultats de recherche. 
    with open("./videos.json","r", encoding="utf-8") as jsonfile:
        videos = json.load(jsonfile)
        
    if request.method == "POST":
        try: 
            search_string = re.compile(request.form.get("search-terms"), re.IGNORECASE)
        except re.error:
            search_string = re.compile(r".*")
        # re.search return None if no match, hence false when tested
        matched_videos = [ video for video in videos if search_string.search(video["title"]) ] 
        videos = matched_videos
        
    return render_template('search.html', videos=videos)

@app.route("/videos/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        title = request.form["title"]
        url = request.form["url"]
        views = 0

        if os.path.exists("videos.json"):
            with open("videos.json", "r", encoding="utf-8") as f:
                videos = json.load(f)
        else:
            videos = []

        new_id = max([v["id"] for v in videos], default=0) + 1
        videos.append({"id": new_id, "title": title, "url": url, "views": views})

        with open("videos.json", "w", encoding="utf-8") as f:
            json.dump(videos, f, ensure_ascii=False, indent=2)

        return redirect("/videos")

    if request.method == 'GET':
        return render_template('add.html')


@app.route("/videos/<int:id>")
def details_video(id):

    with open("./videos.json","r", encoding="utf-8") as jsonfile:
        videos = json.load(jsonfile)

    for video in videos:
        if video["id"]==id:
            video_a_afficher = video
            break

    return render_template('details_video.html', video=video_a_afficher)
    
@app.route("/videos/modif", methods=["POST"])
def modif_video():

    if os.path.exists("videos.json"):
        with open("videos.json", "r", encoding="utf-8") as f:
            videos = json.load(f)
    else:
        videos = []

    id = int(request.form.get("id"))

    for video in videos:
        if video["id"]==id:
            modifier_video = video
            break
    
    title = request.form["title"]
    url = request.form["url"]
    views = request.form["views"]

    videos[videos.index(modifier_video)]={"id": id, "title": title, "url": url, "views": views}

    with open("videos.json", "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    return redirect("/videos")
    

@app.route("/videos/delete", methods=["POST"])
def delete_video():
    if os.path.exists("videos.json"):
        with open("videos.json", "r", encoding="utf-8") as f:
            videos = json.load(f)
    else:
        videos = []

    id = int(request.form["id"])

    for video in videos:
        if video["id"]==id:
            supprimer_video = video
            break

    videos.remove(supprimer_video)

    with open("videos.json", "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    return redirect("/videos")


# Lancement du serveur : mode debug et hot reload actif.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

