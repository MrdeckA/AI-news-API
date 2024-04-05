import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import abort


def get_openai_blog_posts():
    # Define the URL of OpenAI's blog
    url = "https://www.openai.com/blog/"

    # Send an HTTP request to the URL and get the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    posts = []

    # Find all the blog posts
    blog_posts = soup.select(".container .ui-list li")

    for key, post in enumerate(blog_posts):
        # Extract data from each post
        link = post.find("a")['href']
        image = post.find("img")['src']
        title = post.find("h3").get_text(strip=True)
        publication_date = post.find("span").get_text(strip=True)

        # Add post data to the list of articles
        posts.append({
            'id' : key+1,
            'link': f"https://openai.com{link}" ,
            'image': image,
            'title': title,
            'publication_date': publication_date
        })
    return posts


def get_openai_blog_posts_titles():
    # Define the URL of OpenAI's blog
    url = "https://www.openai.com/blog/"

    # Send an HTTP request to the URL and get the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    posts = []

    # Find all the blog posts
    blog_posts = soup.select(".container .ui-list li")

    for post in blog_posts:
        # Extract data from each post
        title = post.find("h3").get_text(strip=True)

        # Add post data to the list of articles
        posts.append(title)
    return posts



def get_one_post_content(url :  str):
    # Define the URL of OpenAI'urls blog

    # Send an HTTP request to the URL and get the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    post_content = soup.find(id='content')

    return post_content.get_text(strip=True)








def analyse_sentiment(article_content):
    
    """
    Analyse le sentiment du contenu de l'article.
    Retourne un score de sentiment (positif, neutre, négatif).
    """
    # Initialiser l'analyseur de sentiment
    analyzer = SentimentIntensityAnalyzer()


    # Analyser le sentiment du texte de l'article
    sentiment_score = analyzer.polarity_scores(article_content)

    # Interpréter le score de sentiment
    if sentiment_score['compound'] >= 0.05:
        return "positif"
    elif sentiment_score['compound'] <= -0.05:
        return "négatif"
    else:
        return "neutre"



def analyse_sentiment_for_a_post(number : int):
     
    """
    Analyse le sentiment du contenu d'un article...
    """
    posts = get_openai_blog_posts()
    if number < 1 or number > len(posts):
        abort(404, description="Post not found")
        
    post = next((post for post in posts if post["id"] == number), None)
    post['content']  = get_one_post_content(post['link'])
    post['sentiment'] = analyse_sentiment(article_content=post['content'])
    return post
