
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

def phi3(message):
    # Point to the local server
    client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    completion = client.chat.completions.create(
      model="microsoft/Phi-3-mini-4k-instruct-gguf",
      messages=[
        {"role": "system", "content": "Always answer in rhymes."},
        {"role": "user", "content": "Introduce yourself."}
      ],
      temperature=0.7,
    )
    return completion.choices[0].message.content


def text(id):
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    
    classes = []
    
    wd = webdriver.Chrome(options=chrome_options)
    
    wd.get("https://timetabling.northampton.ac.uk/CAFStudentTimetables/EnterCAFStudentCalView.aspx?selectedYearId=B&menutype=stu&previousPage=Menu+page&site=External&selectedArea=Student+calendar+view")
    
    button = wd.find_element(value="ctl00_ContentPlaceHolder_StudentIdTextBox")
    button.send_keys('22405755')
    
    submit =  wd.find_element(value="ctl00_ContentPlaceHolder_timetableButton")
    submit.click()
    
    table = wd.find_elements( by=By.CLASS_NAME, value="fc-event-inner")
    for i in table:
        print(i.click())
    
    ques = wd.find_elements(by=By.CLASS_NAME, value="qtip")
    for i in ques:
        classes.append(i.text)
    return classes

class ActionTellTime(Action):
    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        events = tracker.events
        
        # Iterate backwards to find the last bot utterance
        for e in reversed(events):
            if e["event"] != "bot":
                #last_bot_response = e["text"]
                break

        return_classes = text(2283010)
        strr = ""
        for strrr in return_classes:
            strr += "\n" + strrr
            
        dispatcher.utter_message(text=strr)

        return []
    


def get_internships():
    # URL to scrape
    url = "https://www.brightnetwork.co.uk/search/?s=ai+internship"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the internship listings
    internship_listings = soup.find_all("div", class_="col-10 col-lg-8 description")

    # Extract the relevant information from each internship listing
    print('I see you are looking for internships, here are 5 internships from Brightnetwork ( https://www.brightnetwork.co.uk/search/?s=ai+internship ) click the link on each to see further details')

    top_five = []

    for i, listing in enumerate(internship_listings[:5]):  # Only display the first 5 listings

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
        return "action_get_internships"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return_classes = get_internships()
        strr = ""
        for strrr in return_classes:
            strr += "\n" + strrr
            
        dispatcher.utter_message(text=strr)

        return []