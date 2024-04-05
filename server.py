from flask import Flask, jsonify, abort
from utils import get_openai_blog_posts, get_openai_blog_posts_titles, get_one_post_content, analyse_sentiment_for_a_post 

app = Flask(__name__)


@app.route("/get_data")
def get_data():
    """
    Récupère une liste de tous les articles disponibles.
    """
    return jsonify(get_openai_blog_posts_titles())

@app.route("/articles")
def get_articles():
    """
    Affiche des informations sur tous les articles disponibles.
    """
    posts = get_openai_blog_posts()
    return jsonify({'total': len(posts), 'posts': posts})

@app.route("/article/<int:number>")
def get_article(number):
    """
    Affiche le contenu d'un article spécifié par son numéro.
    """
    posts = get_openai_blog_posts()
    if number < 1 or number > len(posts):
        abort(404, description="Post not found")
    
    post = next((post for post in posts if post["id"] == number), None)
    post['content']  = get_one_post_content(post['link'])
    return  post
    

@app.route("/ml/<int:number>")
def get_sentiment(number):
    """
    Exécute un script d'analyse de sentiment pour analyser un article
    """
    post = analyse_sentiment_for_a_post(number)
    return jsonify(post)

if __name__ == "__main__":
    app.run(debug=True)
