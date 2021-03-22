from app import db


class StatusPayload(db.Model):
    __tablename__ = 'statuspayloads'

    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('orderstatuses.id'))
    payload = db.Column(db.Text)

    def __repr__(self) -> str:
        return f"<StatusPayload {self.id!r}: {self.payload}"
