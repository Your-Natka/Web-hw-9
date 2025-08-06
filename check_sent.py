from mongoengine import connect
from db.models import Contact

connect(db="contacts_db", host="mongodb://localhost:27017/contacts_db", alias="default")

print("✅ Відправлені контакти:")
for c in Contact.objects(is_sent=True):
    print(f"✔️ {c.fullname} — {c.send_method} — {c.email or c.phone}")