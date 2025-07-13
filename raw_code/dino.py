import pandas as pd
import requests  #connect to the website get data
from  bs4 import BeautifulSoup # internet site data extraction ,clean HTML data
import time #measuring time
import numpy as np
from openpyxl.workbook import Workbook  #create excel
import re  #
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
url = 'https://en.wikipedia.org/wiki/List_of_dinosaur_genera'
html = requests.get(url)
soup = BeautifulSoup(html.text,'html.parser')  #parser - understand and organise html data
urls = soup.find_all('a', href=True)
links_and_names = [(i['href'], i.text) for i in urls]  #link and text
dino_data_clean = [links_and_names[link] for link in range(len(links_and_names)) if links_and_names[link][0].startswith("/wiki/")]
dino_data_clean = dino_data_clean[:2317:]
dino_df = pd.DataFrame(dino_data_clean, columns = ['url', 'dinosaur'])
dino_df['dinosaur'] = dino_df['dinosaur'].replace('', np.nan)
dino_df = dino_df.dropna(axis = 0, subset = ['dinosaur'])  #dropna - function to remove nullvalue  axis = 0  - checking row wise 1 - col
dino_data_clean = dino_df.set_index('url')['dinosaur'].to_dict()
dino_data = [('https://en.wikipedia.org'+ url, dinosaur) for url, dinosaur in dino_data_clean.items()]
dino_data = dino_data[33::]
dino_urls = [element for pair in dino_data for element in pair if element.startswith('https://en.wikipedia.org')]
dino_info = []
for url in range(200):
    html = requests.get(dino_urls[url])
    soup = BeautifulSoup(html.text, 'html.parser')
    paragraphs = soup.select('p')
    #first we get all paragraphs from the article using .text and strip() to clean the text.
    clean_paragraphs = [paragraph.text.strip() for paragraph in paragraphs]
    #The we use slicing list to get the first 4 paragraphs hoping the real 1st paragraph is there. Fortunatelly after running this script we had successs.
    clean_paragraphs = clean_paragraphs[:4:]
    #We append every paragraph to a list of paragraphs
    dino_info.append(' '.join(clean_paragraphs))
dino_df = pd.DataFrame(dino_data, columns = ['URL','Dinosaur'])
dino_details = pd.DataFrame(dino_info, columns = ['Info'])
dino_df = pd.concat([dino_df, dino_details], ignore_index = True, axis = 1)
dino_df = pd.DataFrame(dino_data, columns = ['URL','Dinosaur'])
dino_details = pd.DataFrame(dino_info, columns = ['Info'])
dino_df = pd.concat([dino_df, dino_details], ignore_index = True, axis = 1)
file_name = r'C:\Users\dhana\Downloads\dino_project.xlsx'
dino_df.to_excel(file_name)
print('DataFrame is written to Excel File successfully!')
dino_df = pd.read_excel(file_name)
dino_df.drop('Unnamed: 0', inplace=True, axis=1)
dino_df.columns = ['URLs', 'Dinosaur', 'Info']
dino_info = dino_df['Info'].to_dict()
print(dino_info)
dino_info = dino_info.values()
heights_clean = []
weights_clean = []
for element in dino_info:
    text = str(element)

    # Extract height
    heights= re.findall(r'\d+\smeters', text)

    if heights:
        heights_clean.append(heights[0])

    else:
        heights_clean.append("-")


    weights=re.findall(r'\d+\stonnes|\d+\skilograms',text) #| means or

    if weights:
        weights_clean.append(weights[0])
    else:
        weights_clean.append('-')
dino_df.drop('Info', axis=1, inplace=True)
dino_df['Height'] = heights_clean
dino_df['Weight'] = weights_clean
dino_df.to_excel(file_name)
print('DataFrame successfully exported to CSV file!')
filtered_df = dino_df[(dino_df['Height'] != '-') | (dino_df['Weight'] != '-')]

print(filtered_df)
# Filter rows where at least one of Height or Weight is not '-'
filtered_df = dino_df[(dino_df['Height'] != '-') | (dino_df['Weight'] != '-')]

# Reset index
filtered_df = filtered_df.reset_index(drop=True)

# Show the result
print(filtered_df)
print(filtered_df.to_string(index=False))
