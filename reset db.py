from app import db, AdminAccount

db.session.query(AdminAccount).delete()
db.session.commit()

