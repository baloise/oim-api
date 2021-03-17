from app import db


class StatusPayload(db.Model):
    __tablename__ = 'statuspayloads'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_id = db.Column(db.Integer, db.ForeignKey('orderstatuses.id'))
    status = db.relationship("OrderStatus", back_populates="payload", uselist=False)
    payload = db.Column(db.Text)

    def __repr__(self) -> str:
        return f"<StatusPayload {self.id!r}: {self.payload}"
