# grcAssist.py
# GRC Relevant News Assist

#This program is designed to pull relevant current news articles for keywords defined in a keywords.csv fie.
#GRC professionals can use this to build a bank of quic-to-access relevant cyber news stories or for a Just-in-Time news story to educate end users.

#The python file is called grcAssist.py.
#The keywords.csv file should have keyword(s) per row.  
#Multiple keywords should be placed on same row with a %20 separating keywords
#e.g. cybersecurity   OR cybersecurity%20healthcare
#IF you have row 1 say cybersecurity and row 2 say healthcare, the script will run two separate queries, one for cybersecurity and one for healthcare. This will likely result in less helpful stories.
#The grcdata.csv file is the output file that the script appends to. It has 5 columns. date,keyword,title,desc,url
#all 3 files should be in the same directory.
#run "python grcAssist.py"
#Python 3

#You need to register a free tier API key from newsdata.io. 
#You get 200 API pulls a day and each story counts as 10 pulls (per newsdata.io site)
#I'd suggest checking API terms when creating your free API key.

# https://newsdata.io/
# Replace your api key in script with the one issued you by Newsdata.io

#Gerald Auger, 7/22/24, SimplyCyber.io

import csv
import requests
import datetime
from openpyxl import Workbook 

def search_news(keyword, api_key, category="technology", language="en"):
  """
  Searches NewsData.io API for a keyword and returns relevant articles.

  Args:
      keyword: The keyword to search for (e.g., "cybersecurity").
      api_key: Your NewsData.io API key.
      category: Optional category to filter results (defaults to "technology").
      language: Optional language parameter (defaults to "en").

  Returns:
      A list of dictionaries, each containing headline, description, and url.
  """
  url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={keyword}&language={language}&category={category}"
  response = requests.get(url)
  print(url)

  try:
    data = response.json()
    articles = []
    if data["status"] == "success":
      for article in data["results"]:
        articles.append({
          "headline": article["title"],
          "description": article["description"],
          "url": article["link"],
        })
      # Write articles to spreadsheet
      filename = "grcdata.csv"
      write_to_spreadsheet(articles, filename, keyword)
    return articles
  except (requests.exceptions.RequestException, KeyError):
    print(f"Error: An error occurred while fetching data from the API.")
    return []

def write_to_spreadsheet(articles, filename, keyword):
  """
  Writes a list of articles to a spreadsheet file.

  Args:
      articles: A list of dictionaries containing article data.
      filename: The filename for the spreadsheet.
  """
  today = datetime.date.today().strftime("%Y-%m-%d")
  with open(filename, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for article in articles:
      writer.writerow([today, keyword, article["headline"], article["description"], article["url"]])


def main():
  """
  Reads keywords from a CSV file or user input and searches for cybersecurity news.
  """
  # Get keywords (modify to read from CSV or get user input)
  keywords_file = "keywords.csv"  # Replace with your filename
  keywords = []
  with open(keywords_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
      keywords.append(row[0])

  # Alternatively, get keywords from user input
  # keywords = input("Enter keywords separated by commas: ").split(",")

  api_key = "YOUR_API_KEY_HERE"  # Replace with your actual NewsData.io API key

  for keyword in keywords:
    articles = search_news(keyword.strip(), api_key)
    if articles:
      print(f"\nSearch results for '{keyword}':")
      for article in articles:
        print(f"\t- {article['headline']}")
        print(f"\t\t{article['description']}")
        print(f"\t\t{article['url']}\n")
    else:
      print(f"No articles found for '{keyword}'.")


if __name__ == "__main__":
  main()
