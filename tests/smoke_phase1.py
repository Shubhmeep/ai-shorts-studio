from app import create_app


def main():
    app = create_app()
    client = app.test_client()

    home_response = client.get("/")
    health_response = client.get("/health")

    assert home_response.status_code == 200
    assert health_response.status_code == 200
    assert health_response.get_json() == {"status": "ok"}

    print("Phase 1 smoke test passed.")


if __name__ == "__main__":
    main()
