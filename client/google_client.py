from dataclasses import dataclass
import requests

from settings import Settings
from schema import GoogleUserData


@dataclass
class GoogleClient:
    settings: Settings

    def get_user_info(self, code: str) -> GoogleUserData:
        """Retrieves user information from Google using authorization code.

        Args:
            code: Authorization code received from Google OAuth2 redirect

        Returns:
            GoogleUserData: Validated user information from Google

        Raises:
            HTTPException: If API request fails or returns invalid response
            ValidationError: If user data doesn't match expected schema
        """
        access_token = self._get_access_token(code=code)
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        return GoogleUserData(**user_info.json(), access_token=access_token)

    def _get_access_token(self, code: str) -> str:
        """Exchanges authorization code for access token from Google OAuth2 endpoint.

        Args:
            code: Authorization code received from Google OAuth2 redirect

        Returns:
            str: Access token for Google API requests

        Raises:
            HTTPException: If token exchange fails or returns invalid response
        """

        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        return response.json()["access_token"]
