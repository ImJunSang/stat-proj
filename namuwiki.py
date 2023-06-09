import time
import csv
import os
from glob import glob

from selenium import webdriver, common
from selenium.webdriver.common.by import By

from stations_n import stations
from tqdm import tqdm

def main(keyword: str, from_index = None):
  if from_index == 0:
    return
  
  driver = webdriver.Chrome()
  if from_index == None:
    driver.get(f"https://namu.wiki/history/{keyword}")
  else:
    driver.get(f"https://namu.wiki/history/{keyword}?from={from_index}")
  
  history_list = None
  timer = 0

  while history_list is None:
    time.sleep(1)
    try:
      history_list = driver.find_element(By.TAG_NAME, 'article').find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'li')
    except (common.exceptions.NoSuchElementException, common.exceptions.InvalidSessionIdException):
      pass
    timer += 1
    if timer > 5:
      # Retry
      driver.quit()
      main(keyword, from_index)
      return

  with open(f'namuwiki/{keyword}.csv', 'w' if from_index == None else 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
    if from_index == None:
      writer.writerow(["index", "timestamp",  "user"])
    
    index = ""
    for history in history_list:
      timestamp = history.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
      index = history.find_element(By.TAG_NAME, 'strong').text
      user = history.find_element(By.XPATH, 'div/div/a').text
      
      writer.writerow([index, timestamp, user])
  
  driver.quit()

  next_index = int(index.split('r')[1]) - 1
  main(keyword, next_index)

if __name__ == "__main__":

  for keyword in tqdm(stations):
    if os.path.isfile(f"namuwiki/{keyword}.csv"):
      continue
    else:
      print(f"Start {keyword}")
      main(keyword)

  for file in glob("namuwiki/*.csv"):
    filename = file.split("\\")[1].split(".")[0]
    if filename not in stations:
      print(filename + " is not in stations list")
      os.remove(file)