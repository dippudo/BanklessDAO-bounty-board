import requests
from bs4 import BeautifulSoup
import json

from datetime import datetime
import calendar

from collections import Counter
from matplotlib import pyplot as plt
import pandas as pd

from io import BytesIO
import uuid, base64

def get_chart():
    url = r"https://www.bountyboard.xyz/api/bounties"
    headers = {"User-Agent": "Mozilla/5.0"}


    response = requests.get(url, headers=headers)
    decoded_reponse = response.json()
    data = decoded_reponse.get("data")


    bounties_created = [] # list of lists containg id and creation date
    bounties_claimed = [] # list of lists containg id and creation date

    key_created = "createdAt"
    key_claimed = "claimedAt"

    for status_update in data:
        
        # collect ids and dates of bounties created
        if key_created in status_update.keys():
            bounties_created.append([status_update.get("_id"), status_update.get(key_created)])

        # collect ids and claim dates of bounties
        if key_claimed in status_update.keys():
            bounties_claimed.append([status_update.get("_id"), status_update.get(key_claimed)])


    # Search for bounties created in the whole year of 2022
    bounties_created_2022 = [] # list of lists contating bounty id and month created

    for bounty in bounties_created:
        created_time = datetime.fromisoformat(bounty[1])
        time = [created_time.year, created_time.month, created_time.day, created_time.hour, created_time.minute, created_time.second]

        if time[0] == 2022:
            bounties_created_2022.append([bounty[0], time[1]])


    # add the months into a list
    bounties_created_monthly_count = []
    for bounty in bounties_created_2022:
        bounties_created_monthly_count.append(bounty[1])

    # count the number of times each month appeared in the list
    count = Counter(bounties_created_monthly_count)


    # convert the integers into months
    months = []
    months_abbrev = []

    for month in count.keys():
        months.append(calendar.month_name[month])
        months_abbrev.append(calendar.month_abbr[month])


    # get the amount of bounties per month
    bounties_per_month = count.values()

    # convert into Pandas DataFrame
    df = pd.DataFrame(data=zip(months, months_abbrev, bounties_per_month), columns=["month", "month_abbrev", "bounties"])


    # plot

    # for web
    plt.switch_backend('AGG')


    plt.style.use("seaborn-ticks")

    plt.figure(figsize=(30, 20))

    df.plot.bar(x="month_abbrev", y="bounties", color="red", legend=None)

    plt.title("BanklessDAO Bounties Created per Month (2022)", pad=20)
    plt.xlabel("Month", labelpad=10)
    plt.ylabel("Bounties", labelpad=15)

    y_ticks = range(0, 51, 3)
    plt.yticks(y_ticks)
    plt.rc('ytick', labelsize=8)

    plt.grid()
    plt.tight_layout()

    # web
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    
    return graph
