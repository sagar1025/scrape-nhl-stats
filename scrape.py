"""
fetch NHL stats from https://www.hockey-reference.com/ and save the data in individual csv files.
"""

import requests
from bs4 import BeautifulSoup
import csv

header = ["Rk","Opponent","GP","W","L","T","OL","PTS","PTS%","GF","GA","GF/G","GA/G","Games"]

#hockey reference only has stats from 1993 onwards :)
for year in range(1993,2022):
    filename = "./s" + str(year) + ".csv"
    
    URL = "https://www.hockey-reference.com/teams/TBL/XXXX_headtohead.html#head2head".replace('XXXX', str(year))
    #fetch url
    page = requests.get(URL)
    #proceed if http 200
    if page.status_code == 200:
        #create new file with header
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerow(header)

        #parse html data.
        soup = BeautifulSoup(page.content, "html.parser")

        #init row data
        data_to_write = []
        #find the table which has the data.
        data_rows = soup.find(id="head2head").find("tbody").find_all("tr")

        if data_rows:
            rnk = 1
            for row in data_rows:
                cells = row.find_all("td")
                
                data = [rnk]

                for idx in range(len(cells)):
                    cell_data = cells[idx].get_text()
                    data.append(cell_data)

                data_to_write.append(data)

                rnk = rnk + 1

            with open(filename, "w", newline='') as fh:
                writer = csv.writer(fh)
                writer.writerows(data_to_write)