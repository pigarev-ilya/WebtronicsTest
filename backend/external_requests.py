import requests
from django.conf import settings


def verify_email(email):
    hunter_io_uri = f'https://api.hunter.io/v2/email-verifier?email={email}' \
                    f'&api_key={settings.HUNTER_IO_KEY}'
    email_verify_response = requests.get(hunter_io_uri)
    status = email_verify_response.json()['data'].get('status')
    return status


def auto_user_info(email):
    clearbit_com_uri = f'https://person.clearbit.com/v2/combined/find?email={email}'
    user_auto_name_response = requests.get(clearbit_com_uri,
                                           headers={'Authorization': f'Bearer {settings.CLEARBIT_API_KEY}'})
    user_info = user_auto_name_response.json()
    return user_info
