from flask import Flask, request, jsonify
from mongoengine import connect
from db.models import Author, Quote, Tag
from http.server import HTTPServer, BaseHTTPRequestHandler


app = Flask(__name__)
connect(db="quotes_db", host="mongodb+srv://my2sails:RYY9xTGwccokAH6g@cluster0.gp5445y.mongodb.net/quotes_db")
def run_server():
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, BaseHTTPRequestHandler)
    print("Server running on port 5000...")
    httpd.serve_forever()

@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()

    if not all(k in data for k in ('fullname', 'born_date', 'born_location', 'description')):
        return jsonify({"error": "Missing fields"}), 400

    author = Author(
        fullname=data['fullname'],
        born_date=data['born_date'],
        born_location=data['born_location'],
        description=data['description']
    )
    author.save()
    return jsonify({"message": "Author created"}), 201

@app.route('/quotes', methods=['POST'])
def create_quote():
    data = request.get_json()

    if not all(k in data for k in ('quote', 'author_fullname', 'tags')):
        return jsonify({"error": "Missing fields"}), 400

    author = Author.objects(fullname=data['author_fullname']).first()
    if not author:
        return jsonify({"error": "Author not found"}), 404

    quote = Quote(quote=data['quote'], author=author)

    for tag_name in data['tags']:
        tag = Tag.objects(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            tag.save()
        quote.tags.append(tag)

    quote.save()
    return jsonify({"message": "Quote created"}), 201

if __name__ == "__main__":
    app.run(debug=True)
