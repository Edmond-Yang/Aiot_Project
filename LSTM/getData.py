import random

import requests
from bs4 import BeautifulSoup

# Send a GET request to the website
url = "https://aiot-server-shsjao25ha-de.a.run.app/DataCheck/plants"
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table on the page
table = soup.find('tbody')

# Extract data from the table
data = []
random.seed(100)
def Data():

    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all('td'):
            row_data.append(cell.text.strip())
        data.append(row_data)

    # Print the extracted data
    more_count = 0
    less_count=0
    need = 0
    grow=17
    amount = 15

    for row in data:
        del row[5]
        del row[4]
        del row[0]
        for i in range(len(row)):
            row[i]=float(row[i])

        need = round(need + grow - amount, 2)
        if need >= 0:
            row.insert(0, amount)
            row.insert(0, 0)

            less_count+=1

            if need > 200:
                need = 200
                amount +=5

            if less_count>=2:
                amount +=5
                less_count=1

            more_count=0
        else:
            row.insert(0, amount)
            row.insert(0, abs(need))

            more_count+=1
            if more_count>=2:
                amount -=5
                more_count=1

            need = 0
            less_count=0
        row.insert(0, grow)
        grow+=random.randint(1,4)

    return data


