import csv
from IPython.display import display
import numpy as np
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom


def main():
    pops = openData(
        "h1\\1\\population_utf8.csv", ";")
    speeds = openData(
        "h1\\1\\results-2019-01-nopeustesti.csv", ",")[1:]

    speeds = prepare_speeds_data(speeds)
    data = {}

    for i in pops:
        name = i[0].split(";")[0]
        data[name] = {"municipality": name, "population": i[2]}

    final_data = {k: data[k] for k, v in speeds.items() if k in data.keys()}

    for k, v in final_data.items():
        final_data[k]["DL avg"] = average(speeds[k]["DL avg"])
        final_data[k]["UL avg"] = average(speeds[k]["UL avg"])
        final_data[k]["DL var"] = get_var(speeds[k]["DL avg"])
        final_data[k]["UL var"] = get_var(speeds[k]["UL avg"])

    export_as_json(list(final_data.values()))
    export_as_xml(list(final_data.values()))


def get_var(data):
    data = list(map(lambda x: 0 if x == "n/a" else int(x), data))
    return np.var(data)


def average(data):
    data = list(map(lambda x: 0 if x == "n/a" else int(x), data))
    return np.average(data)


def prepare_speeds_data(data):
    fixed_data = fix_letters(data)
    new_data = {}

    for i in data:
        if i[3] not in new_data:
            new_data[i[3]] = {"municipality": i[3], "UL avg": [], "DL avg": []}

        new_data[i[3]]["DL avg"].append(i[4])
        new_data[i[3]]["UL avg"].append(i[5])

    return new_data


def fix_letters(data):
    for i in data:
        if i[3] != "Joensuu":
            if "ae" in i[3]:
                i[3] = i[3].replace("ae", "ä")
            if "oe" in i[3]:
                i[3] = i[3].replace("oe", "ö")

    return data


def openData(file, d):
    data = []

    with open(file,  errors="ignore") as infile:
        rd = csv.reader(infile, delimiter=d)
        for line in rd:
            data.append(line)

    return data


def export_as_json(data):
    with open("netspeeds.json", 'w+') as file:
        json.dump(data, file,  ensure_ascii=False)


def export_as_xml(data):
    xml = ET.Element("NetSpeedData")
    for i in data:
        municipality = ET.SubElement(xml, "Municipality")
        name = ET.SubElement(municipality, "Name")
        name.text = i["municipality"]
        population = ET.SubElement(municipality, "Population")
        population.text = str(i["population"])
        dlavg = ET.SubElement(municipality, "DLavg")
        dlavg.text = str(i["DL avg"])
        dlvar = ET.SubElement(municipality, "DLvar")
        dlvar.text = str(i["DL var"])

        ulavg = ET.SubElement(municipality, "ULavg")
        ulavg.text = str(i["UL avg"])
        ulvar = ET.SubElement(municipality, "ULvar")
        ulvar.text = str(i["UL var"])

    final_xml = ET.tostring(xml, encoding="unicode")
    final_xml = minidom.parseString(final_xml).toprettyxml(indent="  ")
    with open("netspeeds.xml", "w+") as file:
        file.write(final_xml)


main()
