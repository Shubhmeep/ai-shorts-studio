from app import create_app
from app.extensions import db
from app.models import Video


def main():
    app = create_app()

    assert app.config["DATABASE_URL"], "DATABASE_URL is required for Phase 3."

    with app.app_context():
        sample_hash = "phase3-smoke-test-file-hash"
        video = Video.query.filter_by(file_hash=sample_hash).first()

        if video is None:
            video = Video(
                file_hash=sample_hash,
                filename="phase3-smoke-test.mp4",
                imagekit_file_id="phase3-placeholder",
                original_url="https://example.com/phase3-smoke-test.mp4",
                duration_seconds=60,
                status="uploaded",
            )
            db.session.add(video)
        else:
            video.filename = "phase3-smoke-test.mp4"
            video.status = "uploaded"

        db.session.commit()

        saved_video = Video.query.filter_by(file_hash=sample_hash).one()

        assert saved_video.filename == "phase3-smoke-test.mp4"
        assert saved_video.file_hash == sample_hash

    print("Phase 3 smoke test passed.")


if __name__ == "__main__":
    main()
