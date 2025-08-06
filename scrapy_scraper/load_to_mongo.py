import json
from mongoengine import connect
from db.models import Quote, Author
import os

connect(db="contacts_db", host=f"mongodb://{os.getenv('MONGODB_HOST')}:27017", alias="default")

def load_quotes():
    with open("quotes.json", "r", encoding="utf-8") as f:
        quotes = json.load(f)
        for q in quotes:
            Quote(**q).save()

def load_authors():
    with open("authors.json", "r", encoding="utf-8") as f:
        authors = json.load(f)
        for a in authors:
            Author(**a).save()

if __name__ == "__main__":
    load_authors()
    load_quotes()