import requests
import pprint
import re
from bs4 import BeautifulSoup

email = "leon.ericsson@me.com"
password = "WingeR08"

LOGIN_URL = "https://m.facebook.com/login/device-based/regular/login/?refsrc=https%3A%2F%2Fm.facebook.com%2F&lwv=100&refid=8"
URL = "https://mbasic.facebook.com/groups/dsaljer"


with requests.Session() as session:
    #Get HTML of login page
    login = session.get(LOGIN_URL)
    soup = BeautifulSoup(login.text, 'html.parser')

    #Find & set data values
    inputs = soup.find('form', id='login_form').find_all('input', {'type': ['hidden', 'submit']})
    input_data = {input.get('name'): input.get('value')  for input in inputs}
    input_data['email'] = email
    input_data['pass'] = password

    #Request session with login data
    post = session.post(LOGIN_URL, data=input_data)
    page_html = session.get(URL)
    
    #Extract posts from URL
    soup = BeautifulSoup(page_html.content, 'html.parser')
    
    posts = soup.find_all('div', class_='dw')
    for post in posts:
        print(post.text)

