import requests
from bs4 import BeautifulSoup
import json

# Declarations
url = input()
nextUrl = []  # subject URLs
header = {'User-Agent': 'Mozilla/5.0'}
fileName = url[28:30]  # dynamic filename


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
                    "https://result.smuexam.in/grade.php?subid="+subcode)

    for urliter in nextUrl:
        count = 1
        code = "SUB"
        credit = 0.0
        reg = 0
        name = ""
        html = session.get(urliter.strip(), headers=header)
        soup = BeautifulSoup(html.content, 'html.parser')

        writeTextFile = open("{}.txt".format(fileName), "w")
        writeTextFile.write(soup.find('pre').getText())
        writeTextFile.close()

        readTextFile = open("{}.txt".format(fileName))
        line = readTextFile.readline()
        while line:
            line=line.strip().split()
            if(len(line)==0 or line[0][0:3]=="REG" or line[0][0:3]=="SIK" or line[0][0:3]=="GRA" or line[0][0:3]=="Abb" or line[0][0:3]=="Abs" or line[0][0:3]=="S>=" or line[0][0:3]=="P>=" or line[0][0:3]=="Sto" or line[0][0:3]=="Gra"):
                line = readTextFile.readline()
                continue
            elif(line[0]=="Subject"):
                if(line[1]=="Code"):
                    code=line[3]
                elif(line[1]=="Title"):
                    i = 3
                    while(i < len(line)):
                        name += line[i]+" "
                        i += 1
                elif(line[1]=="Credit"):
                    credit = float(line[3][0:3])
            else:
                Dict = {}  # subject iteration
                reg = int(line[0])
                fullDict[reg] = fullDict.get(reg, {})
                Dict['sub'] = name
                Dict['int'] = line[1]
                Dict['ext'] = line[2]
                Dict['tot'] = line[3]
                Dict['grade'] = line[4]
                Dict['credit'] = credit
                fullDict[reg][code] = Dict
            line = readTextFile.readline()
          
        readTextFile.close()

    jsonDump = open("{}.json".format(fileName), "w")
    jsonDump.write(json.dumps(fullDict))
    jsonDump.close()


if __name__ == "__main__":
    main()
