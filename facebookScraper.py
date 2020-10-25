import requests
import pprint
import re
from bs4 import BeautifulSoup

email = "leon.ericsson@me.com"
password = "WingeR08"

LOGIN_URL = "https://m.facebook.com/login/device-based/regular/login/?refsrc=https%3A%2F%2Fm.facebook.com%2F&lwv=100&refid=8"
URL = "https://mbasic.facebook.com/groups/dsaljer"


#Scrapes URL and returns the html
def scrapePage():
    with requests.Session() as session:
        #Get HTML of login page
        login = session.get(LOGIN_URL)
        soup = BeautifulSoup(login.text, 'html.parser')

        #Find & set data values for login
        inputs = soup.find('form', id='login_form').find_all('input', {'type': ['hidden', 'submit']})
        input_data = {input.get('name'): input.get('value')  for input in inputs}
        input_data['email'] = email
        input_data['pass'] = password

        #Request session to get passed login page and scrape URL
        post = session.post(LOGIN_URL, data=input_data)
        page_html = session.get(URL)
        
        return page_html

#Extract posts from facebook page
def getPosts(url_html):
    #Parse html with beautifulsoup and retrieve posts
    soup = BeautifulSoup(url_html.content, 'html.parser')
    posts = soup.find_all('div', class_='dw')
    post_words = []

    #Create list of words
    for post in posts:
        post_words += post.text.split()
    
    return post_words
    
        
def findBook(book, post_words):
    if book.upper() in (post_word.upper() for post_word in post_words):
        print(True)
    else:
        print(False)


def main():
    url_html = scrapePage()
    post_words = getPosts(url_html)
    findBook("Södra", post_words)

if __name__ == "__main__":
    main()

#Extract posts from desired URL



    

