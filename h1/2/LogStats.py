import re
import json
import time
from urllib import request
import matplotlib.pyplot as plt


def main():
    data = opendata("h1\\2\\oct2019.txt")
    create_pie_chart(data)
    create_bar_chart(data)


def create_pie_chart(data):
    ips = list(set(parse_ips(data)))  # getting only unique ips
    ip_data = collect_ip_data(ips)
    flattened_ips = flatten_data(ip_data)
    country_counts = get_counts(flattened_ips)
    country_counts.sort(key=lambda x: x["count"], reverse=True)
    create_pie(country_counts[:11])  # taking top 10 countries


def create_bar_chart(data):
    time_data = parse_bars_data(data)
    hours = []
    for i in time_data:
        hours.append(i.split(":")[0])

    hours.sort()
    hours_dict = {}

    for i in hours:
        if i not in hours_dict.keys():
            hours_dict[i] = hours.count(i)

    create_bars(hours_dict)


def parse_bars_data(data):
    d = []
    for line in data:
        parts = line.split()
        if len(parts) > 6:
            d.append(parts[6])
    return d


def get_counts(data):
    counts = []
    countries = []

    for i in data:
        if i not in countries:
            country = {"country": i["country"], "count": data.count(i)}
            counts.append(country)
            countries.append(i)  # making it easy to handle no duplicates

    return counts


def flatten_data(data):
    d = []
    for i in data:
        for j in i:
            d.append(j)
    return d


def opendata(fp):
    data = []
    with open(fp) as file:
        data = file.readlines()

    return data


def parse_ips(data):
    ips = []
    patt = re.compile(r"\d+\.\d+\.\d+\.\d+")

    for line in data:
        parts = line.split()
        if len(parts) > 2 and patt.fullmatch(parts[2]):
            ips.append(parts[2])

    return ips


def collect_ip_data(ips):
    data = []

    for i in range(0, len(ips), 100):
        pars = [{"query": ip, "fields": "country"}
                for ip in ips[i:i+100]]
        q = json.dumps(pars)
        q = q.encode("ascii")
        with request.urlopen("http://ip-api.com/batch", q) as req:
            data.append(req.read())

        time.sleep(5)

    resList = [json.loads(r) for r in data]
    return resList


def create_pie(data):
    values = [v["count"] for v in data]
    labels = [v["country"] for v in data]

    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%')
    plt.savefig("hackpie.png")
    plt.show()


def create_bars(data):
    keys = data.keys()
    values = data.values()
    plt.bar(keys, values)
    plt.xlabel("Time", fontsize=16)
    plt.ylabel("Attacks", fontsize=16)
    plt.savefig("hackbar.png")
    plt.show()


main()
