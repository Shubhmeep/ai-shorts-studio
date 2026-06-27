from app import create_app


def main():
    app = create_app()

    assert app.config["SECRET_KEY"]
    assert "DATABASE_URL" in app.config
    assert "SQLALCHEMY_DATABASE_URI" in app.config

    print("Phase 2 smoke test passed.")


if __name__ == "__main__":
    main()
