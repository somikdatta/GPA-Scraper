import requests
from bs4 import BeautifulSoup
import json

# Declarations
url = "https://result.smitcs.in/ex19.php?eid=NOVEMBER/DECEMBER%20SEMESTER%20EXAMINATION%202019"
nextUrl = []  # subject URLs
header = {'User-Agent': 'Mozilla/5.0'}
fileName = url[27:29]  # dynamic filename


def main():
    # declarations
    fullDict = {}  # full dictionary
    # create a new session
    session = requests.Session()
    # get cookie from entry point
    # cookie gets automatically stored in session
    html = session.get(url.strip(), headers=header)
    soup = BeautifulSoup(html.content, 'html.parser')

    for div in soup.find_all("div", {"class": "card-body"}):
        for paragraph in div.select("p"):
            for link in paragraph.select("a"):
                href = link['href']
                subcode = href[href.index('=')+1:]
                nextUrl.append(
                    "https://result.smitcs.in/grade.php?subid="+subcode)

    for urliter in nextUrl:
        # print(urliter)
        count = 1
        code = "SUB"
        credit = 0.0
        reg = 0
        html = session.get(urliter.strip(), headers=header)
        soup = BeautifulSoup(html.content, 'html.parser')

        writeTextFile = open("{}.txt".format(fileName), "w")
        writeTextFile.write(soup.find('pre').getText())
        writeTextFile.close()

        readTextFile = open("{}.txt".format(fileName))
        line = readTextFile.readline()

        while line:
            if(count < 19):
                if(count == 9):
                    code = line.strip().split()[3]  # store subcode
                elif(count == 13):
                    try:  # store subcredit
                        credit = float(line.strip().split()[3])
                    except:
                        break
            elif(count % 2 != 0):
                if(len(line.strip().split()) == 0):
                    break
                Dict = {}  # subject iteration
                try:
                    reg = int(line.strip().split()[0])
                except:
                    break
                fullDict[reg] = fullDict.get(reg, {})
                Dict['int'] = line.strip().split()[1]
                Dict['ext'] = line.strip().split()[2]
                Dict['tot'] = line.strip().split()[3]
                Dict['grade'] = line.strip().split()[4]
                Dict['credit'] = credit
                fullDict[reg][code] = Dict

            line = readTextFile.readline()
            count += 1
        readTextFile.close()

    jsonDump = open("{}.json".format(fileName), "w")
    jsonDump.write(json.dumps(fullDict))
    jsonDump.close()


if __name__ == "__main__":
    main()
