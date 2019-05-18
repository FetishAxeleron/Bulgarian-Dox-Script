# Author : FetishAxeleron


import urllib.request
import bs4 as bs
import time
from collections import defaultdict
import sys
import argparse

regions = {
    "Blagoevgrad" : 43,
    "Burgas" : 93,
    "Varna" : 139,
    "VelikoTarnovo" : 169,
    "Vidin" : 183,
    "Vratsa" : 217,
    "Gabrovo" : 233,
    "Kurdjali" : 281,
    "Kustendil" : 301,
    "Lovech" : 319,
    "Montana" : 341,
    "Pazardjik" : 377,
    "Pernik" : 395,
    "Pleven" : 435,
    "Plovdiv" : 501,
    "Razgrad" : 527,
    "Ruse" : 555,
    "Silistra" : 575,
    "Sliven" : 601,
    "Smolqn" : 623,
    "Sofia_grad" : 721,
    "Sofia_okrag" : 751,
    "StaraZakora" : 789,
    "Dobrich" : 821,
    "Targovishte" : 843,
    "Haskovo" : 871,
    "Shumen" : 903,
    "Qmbol" : 925
}
headers = { 'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; Win64; x64)",
            'Content-Type':"text/html; charset=utf-8"}

def test_region(region):

    for k, v in regions.items():
        if k == region:
            return v

def get_ID(sex, dd, mm, yy, region):

    construct_params = "?a=gen&s={}&d={}&m={}&y={}&n=99&r={}".format(sex,dd, mm, yy , test_region(region))

    r = urllib.request.Request("https://georgi.unixsol.org/programs/egn.php" + construct_params, headers=headers)

    r = urllib.request.urlopen(r)

    return bs.BeautifulSoup(r, features="html5lib")


def store_ID(sex, day, month, year, region):
    soup = get_ID(sex,day,month,year,region)

    ol = soup.find('ol')

    idList = list()

    for i in ol.find_all('li'):
        id = i.text[0:10]
        if(id[0] == '0'):
            id = id[1:]
        idList.append(id)
    return idList

def generateName(idList):
    _url = "https://www2.mon.bg/AdminRD/mon/default.asp?show=show&intLanguageId=1&id_number={}"


    _page = None
    _ppl = defaultdict(list)
    for i in idList:
        try:
            r = urllib.request.Request(_url.format(i), headers=headers)

            r = urllib.request.urlopen(r)
            print("\n-------------------")
            print("Found at " + i)
            print("-------------------")
            page = bs.BeautifulSoup(r, features="html5lib")

            name = page.find("div", align="left")
            name = name.text
            name = name.replace("\n", " ")
            name = name.replace("\xa0", " ")
            name = name.replace("   ", "")
            name = name.replace("  ", " ")

            _ppl[i].append(name)

            for j in page.find_all("tr",bgcolor = "#ffffff"):
                j = j.find('td').text

                j = j.replace("\t", " ")
                j = j.replace("\n", " ")
                j = j.replace("  ", "")
                _ppl[i].append(j)

        except Exception as e:
            continue
    return _ppl

def generate_people(sex, day, month, year, region):
    id = store_ID(sex, day, month, year, region)
    ppl = generateName(id)

    for k in ppl:
        print("\n------------------")
        for i in ppl[k]:
            print(i)
        print("------------------")
        print("---")

def help_me():
    print("Usage : letsSolve.py -d 10 -m 12 -y 1992 -r Haskovo -man/woman\n")
    print("Help : letsSolve -help r\n")

def logo():
    print("""

   .       . .     . .    .     . .     . .     . .     .       .    .  . .
.+'|    .+'|=|`+.+'|=|`+.=|`+.+'|=|`+.+'|=|`+.+'|=|`+.+'|    .+'|  .'.+'|=|`+.
|  |    |  | `+.|.+' |  | `+.|  | `+.|  | `+.|  | |  |  |    |  |  | |  | `+.|
|  |    |  |=|`.     |  |    |  | .  |  | .  |  | |  |  |    |  |  | |  |=|`.
|  |    |  | `.|     |  |    `+.|=|`+`+.|=|`+|  | |  |  |    |  |  | |  | `.|
|  |    |  |    .    |  |    .    |  .    |  |  | |  |  |    |  |  | |  |    .
|  | .+'|  | .+'|    |  |    |`+. |  |`+. |  |  | |  |  | .+'|  | .+ |  | .+'|
`+.|=|.+`+.|=|.+'    |.+'    `+.|=|.+`+.|=|.+`+.|=|.+`+.|=|.+`+.|=|.+`+.|=|.+'

    """)

def test_args(args):
    if(args.d == None or args.m == None or args.y == None or args.r == None or args.s==None):
        sys.exit()
    else:
        day = str(args.d)
        month = str(args.m)
        year = str(args.y)
        region = str(args.r)
        sex = None
        if(str(args.s) == "man"):
            sex = 1
        elif(str(args.s) == "woman"):
            sex = 2
        generate_people(sex, day, month, year, region)

def main():
    logo()
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="set the day, ex d=2", type = str)
    parser.add_argument("-m", help="set the month, ex m=6", type = str)
    parser.add_argument("-y", help="set the year, ex y=1992", type = str)
    parser.add_argument("-r", help="set the region, ex: r=Haskovo", type = str)
    parser.add_argument("-s", help="set the sex, can be either man or a woman. ex : -s man", type = str )
    parser.add_argument("-hs", help="gives you the full list of regions supported python letsSolve.py -hs", action='store_false')
    args = parser.parse_args()
    print("\n Usage : python letsSolve -d 2 -m 6 -y 1992 -r Haskovo -s man")
    test_args(args)

if __name__ == '__main__':
    main()
