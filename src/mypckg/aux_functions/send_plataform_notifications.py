import requests
from requests.auth import HTTPBasicAuth

base_url = "website"
# final_url="/{0}/friendly/{1}/url".format(base_url,any_value_here)


def send_plataform_notification(user, message, types='notification'):

    payload = {'types': types, 'tos': user, 'message': message}
    response = requests.post(base_url, data=payload,
                             auth=HTTPBasicAuth('aut', 'password'))
    if response.status_code == 200:
        return True
    else:
        return False

# print(response.text) #TEXT/HTML
# print(response.status_code, response.reason) #HTTP
