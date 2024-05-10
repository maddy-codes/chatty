
from typing import Any, Text, Dict, List
from datetime import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import pandas as pa
import pandas as pd
from fuzzywuzzy import process
    


def get_internships():
    url = "https://www.brightnetwork.co.uk/search/?s=ai+internship"

    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    internship_listings = soup.find_all("div", class_="col-10 col-lg-8 description")

    print('I see you are looking for internships, here are 5 internships from Brightnetwork ( https://www.brightnetwork.co.uk/search/?s=ai+internship ) click the link on each to see further details')

    top_five = []

    for i, listing in enumerate(internship_listings[:5]):  

        title = listing.find("h3").text.strip()
        company_location = listing.find("span", class_="search-result-row__subtitle").text.strip().split("-")
        company = company_location[0]
        location = company_location[1]
        link = listing.find("a")["href"]
        description = listing.find("p", class_="d-none d-lg-block").text.strip()

        result = "=" * 80 + "\n" + f"Title: {title.strip()}" + "\n" + f"Company: {company.strip()}" + "\n" + f"Location: {location.strip()}" + "\n" + f"Link: https://www.brightnetwork.co.uk{link.strip()}" + "\n" + f"Description: {description.strip()}" + "\n" + "=" * 80

        top_five.append(result)
            
    return top_five

class ActionGetInternship(Action):
    def name(self) -> Text:
        return "scrape_internships"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return_classes = get_internships()
        strr = ""
        for strrr in return_classes:
            strr += "\n" + strrr
            
        dispatcher.utter_message(text=strr)

        return []
    


def get_events():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--disable-extensions")  

    driver = webdriver.Chrome(options=chrome_options)

    url = "https://www.northampton.ac.uk/events/"
    driver.get(url)

    driver.implicitly_wait(10)

    event_divs = driver.find_elements(By.CSS_SELECTOR, "div.col-md-6.col-lg-4.mb-5.mb-md-6")
    end = "" 
    for div in event_divs:
        event_name = div.find_element(By.TAG_NAME, "h3").text

        date_element = div.find_element(By.CSS_SELECTOR, "p.pb-md-5.mb-0.mb-md-4")
        date = date_element.text.strip()

        link = div.find_element(By.TAG_NAME, "a").get_attribute("href")

        end += f"Event Name: {event_name}"
        end += f"Date: {date}"
        end += f"Link: {link}"

    driver.quit()
    return end 
    
class ActionGetEvents(Action):
    def name(self) -> Text:
        return "scrape_events"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        strr = get_events()
            
        dispatcher.utter_message(text=strr)

        return []
    

    
def get_societies():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")  

    driver = webdriver.Chrome(options=chrome_options)

 
    url = "https://northamptonunion.com/societies"
    driver.get(url)

    driver.implicitly_wait(10)

    society_divs = driver.find_elements(By.CSS_SELECTOR, "div.d-flex.justify-content-start.g-bg-teal--hover.g-bg-white.g-rounded-4.g-transition-0_3.g-transition--ease-in-out.g-pa-30")
    end = ""

    for div in society_divs:
        society_name = div.find_element(By.TAG_NAME, "h4").text

        view_more_link = div.find_element(By.LINK_TEXT, "View More").get_attribute('href')


        end += f"Society Name: {society_name}, "
        end += f"View More Link: {view_more_link} , "
    
    driver.quit()
    return end
   


    
class ActionGetSocieties(Action):
    def name(self) -> Text:
        return "scrape_societies"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        strr = get_societies()
            
        dispatcher.utter_message(text=strr)

        return []
    
def get_news():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")  

    driver = webdriver.Chrome(options=chrome_options)

    url = "https://www.northampton.ac.uk/news/"
    driver.get(url)

    driver.implicitly_wait(10)

    news_divs = driver.find_elements(By.CSS_SELECTOR, "div.col-md-6.col-lg-4.mb-5.mb-md-6")
#
    for div in news_divs:
        news_name = div.find_element(By.CSS_SELECTOR, "h3.h6").text

        description_element = div.find_element(By.CSS_SELECTOR, "p.d-none.d-md-block")
        description = description_element.text.strip()

        date_element = div.find_element(By.CSS_SELECTOR, "p.date")
        date = date_element.text.strip()

        link = div.find_element(By.TAG_NAME, "a").get_attribute("href")

        end += f"News Name: {news_name}"
        end += f"Description: {description}"
        end += f"Date: {date}"
        end += f"More information: {link}"
    driver.quit()
    return end

class ActionGetNews(Action):
    def name(self) -> Text:
        return "scrape_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        strr = get_news()
            
        dispatcher.utter_message(text=strr)

        return []
    


def get_details(name):
    df = pd.read_csv('contacts.csv')

    names = df['Name'].tolist()

    closest_match, score = process.extractOne("dr mu mu", names)

    match_row = df[df['Name'] == closest_match].iloc[0]

    match_name = match_row['Name']
    match_faculty = match_row['Faculty']
    match_phone = match_row['Phone']
    match_email = match_row['Email']

    if match_faculty == 'Yes':
        faculty_status = "They are part of the university accommodation or something similar."
    else:
        faculty_status = "They are a person."
    
    return 'name:' +  match_name + ' , faculty: ' + match_faculty + ', phone: ' + match_phone + ', email: '+ match_email + ', faculty_status: ' + faculty_status


class ActionContactPeople(Action):
    def name(self) -> Text:
        return "contact_people"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        strr = get_details('name')
            
        dispatcher.utter_message(text=strr)

        return []