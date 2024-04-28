import firebase_admin
import google
from firebase_admin import credentials
from google.oauth2 import service_account


def _get_access_token():
  credentials = service_account.Credentials.from_service_account_file(
    'serviceAccountKey.json', scopes = ['https://www.googleapis.com/auth/firebase.messaging'])
  request = google.auth.transport.requests.Request()
  credentials.refresh(request)
  return credentials.token
# Example usage with print statements (avoid printing private key)
if __name__ == "__main__":
  filepath = "serviceAccountKey.json"
  cred = credentials.Certificate(filepath)
  firebase_admin.initialize_app(cred)
  print(_get_access_token())
