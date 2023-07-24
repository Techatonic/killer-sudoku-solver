import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("./sudoku-27fa4-firebase-adminsdk-x9h3m-d0db95065b.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def get_document_count_in_collection(collection):
    doc_ref = db.collection(collection).document("data")
    doc = doc_ref.get()
    print(doc)
    if not doc.exists:
        print("No such document")
    data = doc.to_dict()
    document_count = data['documentCount']
    return document_count

document_count = get_document_count_in_collection("killersudokus")
