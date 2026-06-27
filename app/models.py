from datetime import datetime

from app.extensions import db


class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(128), nullable=False, unique=True, index=True)
    imagekit_file_id = db.Column(db.String(255), nullable=True)
    original_url = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="uploaded")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Video id={self.id} file_hash={self.file_hash}>"
