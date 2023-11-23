from mongoengine import Document
from mongoengine import StringField, IntField

class Feedback(Document):
    title = StringField(required=True,max_length=60)
    product_id = IntField()
    description = StringField()

    def __str__(self):
        return f"Product(title={self.title}, product_id={self.product_id}, description={self.description})"