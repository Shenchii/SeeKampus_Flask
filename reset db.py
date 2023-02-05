from app import db, ScProfiles

db.session.query(ScProfiles).delete()
db.session.commit()

