import json, re, os
from flask import Flask, request, render_template, redirect


# Lors du développement d'une app Flask, mettre :
#       les fichiers HTML dans un dossier templates/
#       les fichiers CSS, JS, images dans un dossier static/

# Création de l'application Flask (on indique que ce fichier est le fichier principal).
app = Flask(__name__)       # __name__ : variable spéciale de python contenant le nom de ce fichier.

PLAYLIST_PATH = "videos.json"

def json_videos_loader (path:str=PLAYLIST_PATH) -> list:
    list_videos = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            list_videos = json.load(f)
    else:
        print("file error: Json data file for playlist not found")
    return list_videos

def json_videos_saver (list_videos:list, path:str=PLAYLIST_PATH) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(list_videos, f, ensure_ascii=False, indent=2)
    return None

def search_video_by_id (list_videos:list, identifiant:int) -> dict:
    for video in list_videos:
        if video["id"]== identifiant:
            return video
    ## If not found
    return dict()


@app.route("/")     # Définition de la route principale : http://127.0.0.1:5050/
def index():
    """Retourne le fichier index.html du dossier templates/ grâce à la fonction render_template() de Flask."""
    return render_template('index.html')

@app.route("/videos")
def affiche_videos():
    videos = json_videos_loader()
    return render_template("videos.html", videos=videos)

@app.route("/videos/search", methods=["GET","POST"])
def search():
    # Rechercher des vidéos par titre  
    # Affiche un formulaire de recherche et les résultats de recherche. 
    videos = json_videos_loader()
        
    if request.method == "POST":
        try: 
            search_string = re.compile(request.form.get("search-terms"), re.IGNORECASE)
        except re.error:
            search_string = re.compile(r".*")
        # re.search return None if no match, hence false when tested
        matched_videos = [ video 
                          for video in videos 
                          if search_string.search(video["title"]) 
                         ] 
        videos = matched_videos
        
    return render_template('search.html', videos=videos)

@app.route("/videos/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        videos = json_videos_loader()

        title = request.form["title"]
        url = request.form["url"]
        views = 0
        new_id = max([v["id"] for v in videos], default=0) + 1

        videos.append({"id": new_id, "title": title, "url": url, "views": views})
        json_videos_saver(videos)
        
        return redirect("/videos")

    if request.method == 'GET':
        return render_template('add.html')


@app.route("/videos/<int:id>")
def details_video(id):

    videos = json_videos_loader()
    video_a_afficher = search_video_by_id(videos, id)
    return render_template('details_video.html', video=video_a_afficher)
    
@app.route("/videos/modif", methods=["POST"])
def modif_video():

    videos = json_videos_loader()

    id = int(request.form.get("id"))
    title = request.form["title"]
    url = request.form["url"]
    views = request.form["views"]

    old_video_position=videos.index(search_video_by_id(videos, id))
    
    videos[old_video_position]={"id": id, "title": title, "url": url, "views": views}
    json_videos_saver(videos)
    
    return redirect("/videos")
    

@app.route("/videos/delete", methods=["POST"])
def delete_video():
    
    videos = json_videos_loader(PLAYLIST_PATH)
    id = int(request.form["id"])
    videos.remove(search_video_by_id(videos, id))
    json_videos_saver(videos)

    return redirect("/videos")


# Lancement du serveur : mode debug et hot reload actif.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

