"""MongoEngine моделі для авторів, цитат і тегів"""
# pyright: reportMissingImports=false

from mongoengine import Document, StringField, ListField, ReferenceField, BooleanField, EmailField

class Tag(Document):
    """
    Represents a tag assigned to a quote (e.g., 'life', 'inspiration').
    """
    name = StringField(required=True, unique=True)

    def __str__(self):
        return self.name

class Author(Document):
    """
    Represents an author of quotes.
    """
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

    def __str__(self):
        return self.fullname


class Quote(Document):
    """
    Represents a quote and its relations to an author and tags.
    """
    quote = StringField(required=True)
    author = ReferenceField(Author, required=True, reverse_delete_rule=2)  # CASCADE
    tags = ListField(ReferenceField(Tag))

    def __str__(self):
        return f'"{self.quote}" — {self.author.fullname}'
    
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone = StringField()
    send_method = StringField(choices=["email", "sms"], default="email")
    is_sent = BooleanField(default=False)

    def __str__(self):
        return f"{self.fullname} ({self.send_method}) - {self.email or self.phone}"
    
    email = EmailField(required=True)