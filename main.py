from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
import logging
import openai
import requests
from webdriver_confi import webdriver_config
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY", "default_openai_api_key")

class LoomRequest(BaseModel):
    video_url: str
    prompt: str

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def summarize_text(text, prompt=None):
    default_prompt = "summarize and make proposal from this text and it should look professional"
    prompt_to_use = prompt if prompt else default_prompt
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_to_use + "\n" + text}
        ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
   
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        logging.error("OpenAI API Error: %s", response.text)
        return None
    
@app.post("/download_caption/")
async def download_caption(request: LoomRequest):
    data = []
    
    # Initialize the driver
    driver = webdriver_config() 
    

    wait = WebDriverWait(driver, 10)
    
    driver.get(request.video_url)
    logging.debug(f'Navigating to video URL: {request.video_url}')
    
   
    try:
        transcript_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="sidebar-tab-Transcript"]')))
        transcript_button.click()
        logging.debug("Clicked on the Transcript button")
    except TimeoutException:
        logging.error("Timeout: Transcript button not found or not clickable.")
        driver.quit()
        return {"error": "Transcript button not found or not clickable."}
    
    # Wait for the transcript section to be visible
    try:
        transcripts = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'transcript-list_transcript_1tw')))
    except TimeoutException:
        logging.error("Timeout: Transcript not found.")
        driver.quit()
        return {"error": "Transcript not found."}
    
    # Wait for the caption elements to be visible within the transcript section
    try:
        captions = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'css-y326tu')))
        logging.debug("Captions found")
    except TimeoutException:
        logging.error("Timeout: Captions not found.")
        driver.quit()
        return {"error": "Captions not found."}
    
    # Scroll into view for each caption element
    for caption in captions:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", caption)
        except StaleElementReferenceException:
            continue
            
 
    time.sleep(5)
    
    
    captions = driver.find_elements(By.CLASS_NAME, 'css-y326tu')
    for caption in captions:
        try:
            data.append(caption.text)
        except StaleElementReferenceException:
            continue
    
    driver.quit()
   
    logging.debug(f'Captions found: {data}')
    loom_summary = "\n".join(data)
    chatgpt_response = summarize_text(loom_summary, request.prompt)
    logging.debug(f'proposal made: {chatgpt_response}')
    
    return {"loom_summary": loom_summary, "chatgpt_response": chatgpt_response}