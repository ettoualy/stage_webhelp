# Project : LansWeeper
# Created by Moncef BENAICHA at 7/24/18 - 22:11
# Email : contact@moncefbenaicha.me

from Browser import Browser
from bs4 import BeautifulSoup
import re


class LansWeeper(object):

    def __init__(self, baselink, username=None, password=None):
        self.browser = Browser()
        self.baselink = str(baselink).strip("/") + "/"
        self.browser.open_page(self.baselink + 'login.aspx')
        try:
            if username == None:
                self.browser.sendClick("//input[@id='defaultuser']")
            else:
                self.__login(username, password)
        except:
            pass

    def __login(self, username, password):
        self.browser.sendData(username, "//input[@id='NameTextBox']")
        self.browser.sendData(password, "//input[@id='PasswordInput']", True)

    def getAssestsLInks(self):
        page = BeautifulSoup(self.browser.getContent(self.baselink + "Assets.aspx"), "html5lib")
        assests = page.find(id="appendbody").find_all("tr")
        links = []
        for assest in assests:
            links.append(assest.a["href"])
        return links

    def getAssestsData(self, link):
        myassest = {
            'Asset Type': "",
            'Domain': "",
            'OS': "",
            'Build': "",
            'Version': "",
            'Manufacturer': "",
            'Model': '',
            'SKU': '',
            'Memory': '',
            'Processor': '',
            'Motherboard': '',
            'Graphics': '',
            'Audio': '',
            'Antivirus': '',
            'Network': '',
            'Harddisk': '',
        }
        page = BeautifulSoup(self.browser.getContent(self.baselink + link), "html5lib")
        try:
            table = page.find(id="assetcontent").find("table", class_="compmenu").find_next_sibling("table").find_all("td")
        except:
            raise Exception("Table not found")
        for element in table[0].find_all("tr"):
            td = element.find_all("td")
            key = re.sub(' +'," ",str(td[0].contents[0].string).rstrip(":")).strip(" ")
            if key in myassest.keys():
                if key in ("Asset Type", "Last user", "Domain", "Manufacturer", "Model"):
                    myassest[key] = str(td[1].a.string).replace("\n", " ").replace("\r", " ").strip(" ")
                elif key in ("Antivirus", "Network"):
                    item = td[1].find_all("span")
                    nbr_items = int(len(item) / 3)
                    itemlist = []
                    j = 0
                    for i in range(0, nbr_items):
                        software = '{} {} {}'.format(item[j].string.replace("\n", " ").replace("\r", " ").strip(" "),
                                                     item[j + 1].string.replace("\n", " ").replace("\r", " ").strip(
                                                         " "),
                                                     item[j + 2].string.replace("\n", " ").replace("\r", " ").strip(
                                                         " "))
                        j += 3
                        itemlist.append(software)
                    myassest[key] = re.sub(' +', ' ', ';'.join(itemlist))
                elif key == "Harddisk":
                    harddrives = td[1].find_all("table", recursive=False)
                    harddrives_labels = td[1].find_all("img", recursive=False)
                    HD_lists = []
                    j = 0
                    for drive in harddrives:
                        HD = str(harddrives_labels[j].next_sibling).replace("\n", " ").replace("\r", " ").strip(
                            " ") + str(
                            drive.find_all("tr")[0].find_all("td", recursive=False)[1].span.string).replace("\n",
                                                                                                            " ").replace(
                            '\xa0', '').replace("\r", " ").strip(" ")
                        j += 1
                        HD_lists.append(HD)
                    myassest[key] = re.sub(' +', ' ', ';'.join(HD_lists))
                else:
                    myassest[key] = re.sub(" +", " ", str(td[1].img.next_sibling).replace("\n", " ").replace("\r", " ").strip(" "))
        return myassest
