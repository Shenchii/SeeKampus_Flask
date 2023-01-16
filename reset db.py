from app import db, DTSchool

db.session.query(DTSchool).delete()
db.session.commit()

