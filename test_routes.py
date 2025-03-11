from app import app

def test_routes():
    with app.test_client() as client:
        # Test login page
        login_response = client.get('/login')
        print(f"Login status code: {login_response.status_code}")
        print(f"Login data: {login_response.data}")

        # Test register page
        register_response = client.get('/register')
        print(f"Register status code: {register_response.status_code}")
        print(f"Register data: {register_response.data}")

if __name__ == "__main__":
    test_routes() 