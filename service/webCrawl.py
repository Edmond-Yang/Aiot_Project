import requests
from bs4 import BeautifulSoup
import json
import datetime


class plant_bug():
    def __init__(self, plant):
        self.name = "Bug"
        self.plantname = plant
        self.requests = requests.get(
            "http://kplant.biodiv.tw/{}/{}.htm".format(plant, plant))
        self.requests.encoding = "utf-8"
        self.soup = BeautifulSoup(self.requests.text, "html.parser")


class weather_bug():
    def __init__(self, location):
        self.name = "Weather"
        self.location = location
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=rdec-key-123-45678-011121314"
        self.requests = requests.get(url)
        j = json.loads(self.requests.text)[
            "records"]["locations"][0]["location"]
        for d in j:
            if d["locationName"] == self.location:
                self.data = d
                break
            
    def __call__(self):
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=rdec-key-123-45678-011121314"
        self.requests = requests.get(url)
        j = json.loads(self.requests.text)[
            "records"]["locations"][0]["location"]
        for d in j:
            if d["locationName"] == self.location:
                data = d
                break
            
        print(data["weatherElement"][0])
        result={
            'location': self.location, 
            'description': data["weatherElement"][0]['description'],
            'start': data["weatherElement"][0]['time'][0]['startTime'],
            'end': data["weatherElement"][0]['time'][0]['endTime'],
            'value': data["weatherElement"][0]['time'][0]["elementValue"][0]["value"],
                }
        
        return result

    def today_data(self):
        data = {"locationName": self.location, "weatherElement": []}
        for ele in self.data["weatherElement"]:
            data_ele = {"description": ele["description"], "time": []}
            for t in ele["time"]:
                if str(datetime.date.today()) in t["startTime"]:
                    data_ele["time"].append(t)
            data["weatherElement"].append(data_ele)
        return data

    def csv_list(self):
        output = ["地點,項目,開始時間,結束時間,數值\n"]
        data = self.today_data()
        for weatherElement in data["weatherElement"]:
            data_ele = "{},{}".format(
                self.location, weatherElement["description"])
            for time in weatherElement["time"]:
                output_ele = data_ele + \
                    ",{},{},{}\n".format(
                        time["startTime"], time["endTime"], time["elementValue"][0]["value"])
                output.append(output_ele)
        return output


if __name__ == "__main__":
    plant = "狐尾武竹"
    p_bug = plant_bug(plant)
    sel = p_bug.soup.select("p.MsoNormal")

    location = "臺中市"
    w_bug = weather_bug(location)
    print(w_bug.csv_list())

    with open("location_today_weather.csv", "w", encoding="big5")as f:
        for i in w_bug.csv_list():
            f.write(i)

    print(w_bug.data)
