from google.cloud import firestore

db = firestore.Client(project="genibuilder", database="default")

try:
    docs = db.collection("item").stream()
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
except Exception as e:
    print("Error:", e)
