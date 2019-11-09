import matplotlib.pyplot as plt
from urllib import request
import xml.etree.ElementTree as ET
from io import BytesIO


def main():
    unemployment_data = parse_data(
        get_data("http://api.worldbank.org/countries/fin/indicators/SL.UEM.TOTL.ZS"))
    gdp_data = parse_data(
        get_data("http://api.worldbank.org/countries/fin/indicators/NY.GDP.MKTP.CN"))

    # sorting by date
    unemployment_data.sort(key=lambda x: str(x))
    gdp_data.sort(key=lambda x: str(x))

    create_chart(unemployment_data, gdp_data)


def create_chart(unemployment_data, gdp_data):
    fig, ax1 = plt.subplots()

    unemployment_keys = [list(k.keys())[0] for k in unemployment_data]
    unemployment_values = [list(v.values())[0] for v in unemployment_data]
    gdp_keys = [list(k.keys())[0] for k in gdp_data]
    gdp_values = [list(v.values())[0] for v in gdp_data]

    color = "tab:blue"
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Unemployment (% of labor force)", color=color)
    ax1.plot(unemployment_keys, unemployment_values,
             label="Unemployment", color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()

    color = "tab:orange"
    ax2.set_ylabel('GDP (local currency)', color=color)
    ax2.plot(gdp_keys, gdp_values, label="GDP", color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    ax1.legend(loc=2)
    ax2.legend(loc=1)

    fig.tight_layout()
    plt.show()
    # save_plot(fig)


def get_data(url):
    xml_data = []
    page = 1

    req_data = do_request(url)
    root = ET.parse(BytesIO(req_data)).getroot()
    pages = int(root.attrib["pages"])
    xml_data.append(root)

    while page < pages:
        page += 1
        req_data = do_request(url + "?page="+str(page))
        root = ET.parse(BytesIO(req_data)).getroot()
        xml_data.append(root)

    return xml_data


def do_request(url):
    return request.urlopen(url).read()


def parse_data(data):
    parsed_data = []

    for i in data:
        for child in i:
            date = child.find("{http://www.worldbank.org}date").text
            value = child.find("{http://www.worldbank.org}value").text
            if value == None:
                value = 0
            parsed_data.append({int(date): float(value)})
    return parsed_data


def save_plot(fig):
    fig.savefig("unemployment_vs_gdp.pdf", format="pdf")


main()
