import requests
import pprint
import re
import sys
import smtplib, ssl
from bs4 import BeautifulSoup


LOGIN_URL = "https://m.facebook.com/login/device-based/regular/login/?refsrc=https%3A%2F%2Fm.facebook.com%2F&lwv=100&refid=8"
URL = "https://mbasic.facebook.com/groups/dsaljer"


#Scrapes URL and returns the html
def scrapePage(email, password):
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
        session.post(LOGIN_URL, data=input_data)
        page_html = session.get(URL)
        
        return page_html

#Extract post words from facebook page
def getPostWords(url_html):
    #Parse html with beautifulsoup and retrieve posts
    soup = BeautifulSoup(url_html.content, 'html.parser')
    posts = soup.find_all('div', class_='dw')
    post_words = []

    #Create list of words
    for post in posts:
        post_words += post.text.split()
    
    return post_words
    
#Find the requested book among posts       
def findBook(book, post_words):
    if book.upper() in (post_word.upper() for post_word in post_words):
        return True
    else:
        return False

#Send email to user informing them book has been found
def sendEmail():
    #Setup for SSL connection and email 
    port = 465 
    password_gmail = sys.argv[3]
    sender_email = "bookavailableonfacebook@gmail.com"
    reciever_email = "leon.ericsson@me.com"
    message = """\

    There is currently a book available that you are looking for."""

    #Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server:
        server.login(sender_email, password_gmail)
        server.sendmail(sender_email, reciever_email, message)



def main():
    email, password = sys.argv[1] , sys.argv[2]
    
    url_html = scrapePage(email, password) #Get html
    post_words = getPostWords(url_html) #Get words
    #print(post_words)

    if findBook("Elektronik", post_words):
        print(True)
        #sendEmail()


if __name__ == "__main__":
    main()





    

