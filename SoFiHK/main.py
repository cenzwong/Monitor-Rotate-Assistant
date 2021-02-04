# https://deepnote.com/project/45f04c35-7c02-4b4c-8ab0-4c7c55b4f066#%2Fsofi_dailyreport.ipynb

import fitz  # this is pymupdf

def readSoFiReport(pathFile):
    with fitz.open(pathFile) as doc:
        text = ""
        for page in doc:
            text += page.getText()

    #================ Trip the text==========================
    # text.split("\n")
    start = text.find("Stock/Product Position")
    end = text.find("* = Product Suspended")
    trippedtxt = text[start:end]
    return trippedtxt
    
def findStock(textall, stock):
    # start = textall.find(stock)
    listText = textall.split("\n")
    locaion = listText.index(stock)
    # print(listText[locaion+2])
    # print(listText[locaion+2][0].isdigit()) 
    # you cannot use is numeric because it is string
    # is digit only check if digit or not, no "." is allow
    if listText[locaion+2][0].isdigit(): 
        return listText[locaion-4:locaion+3]
    else:
        # this line is to hadle to exceptional case of TSM 
        listText[locaion+1] = listText[locaion+1] + " " +listText[locaion+2]
        listText[locaion+2] = listText[locaion+3]
        return listText[locaion-4:locaion+3] 
        
def getProfolio(textall):
    test_list = textall.split("\n")

    # using filter() + lambda 
    # to get string with substring 
    lastValUp = False
    def myFilterFunc(x):
        isLength = len(x) < 5 and len(x) > 2
        isUp = x.isupper()
        exceptionList = ["USD"]
        isExcept = x in exceptionList
        isOut = isLength and isUp and not isExcept
        
        global lastValUp
        if lastValUp == False:
            lastValUp = isUp
            return isOut
        lastValUp = isUp
        return False

    # res = list(filter(lambda x: len(x) < 5 and len(x) > 2 , test_list)) 
    res = list(filter(myFilterFunc , test_list)) 

    # printing result 
    return res
    
for ticker in getProfolio(readSoFiReport("CenzSoFi.pdf")):
    print(findStock(readSoFiReport("CenzSoFi.pdf"), ticker))
