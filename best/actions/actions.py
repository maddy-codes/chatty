
from typing import Any, Text, Dict, List
from datetime import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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

        current_time = datetime.now().strftime("%H:%M:%S")
        response_message = f"The current time is: {current_time}"
        return_classes = text(22405755)
        strr = ""
        for strrr in return_classes:
            strr += strrr
            
        dispatcher.utter_message(text=strr)

        return []