import time
import csv
import os
from glob import glob

from selenium import webdriver
from selenium.webdriver.common.by import By

from stations_w import stations

def main(keyword: str):
  
  driver = webdriver.Chrome()
  driver.get(f"https://ko.wikipedia.org/w/index.php?title={keyword}&action=history&offset=&limit=3000")
  
  time.sleep(2)

  history_list = driver.find_elements(By.CLASS_NAME, 'mw-changeslist-date')

  total = len(history_list)
  print("Total history count: ", total)

  with open(f'wikipedia/{keyword}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["index", "timestamp",  "user"])

    for i, history in enumerate(history_list):
      timestamp = history.get_attribute("textContent").replace("년 ", "-").replace("월 ", "-").replace("일", "").split(" ")
      timestamp = timestamp[0] + "T" + timestamp[2] + ":00.000Z"
      index = total - i
      
      writer.writerow([index, timestamp, ""])
  
  driver.close()

if __name__ == "__main__":

  for keyword in stations:
    if os.path.isfile(f"wikipedia/{keyword}.csv"):
      continue
    else:
      print(f"Start {keyword}")
      main(keyword)

  for file in glob("wikipedia/*.csv"):
    filename = file.split("\\")[1].split(".")[0]
    if filename not in stations:
      print(filename + " is not in stations list")
      os.remove(file)