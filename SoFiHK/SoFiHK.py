from enum import Enum
import fitz

def help():
    helpText = """
    import SoFiHK
    CenzSoFi = SoFiHK.SoFiDReport("CenzSoFi.pdf")
    CenzSoFi.ReadTable(SoFiHK.PdfTable.Table_Portfolio_Summary)
    CenzSoFi.ReadTable(SoFiHK.PdfTable.Table_Daily_Trade)
    CenzSoFi.ReadTable(SoFiHK.PdfTable.Table_Stock_Product_Position)
    CenzSoFi.ReadTable(SoFiHK.PdfTable.Table_Stock_Product_Position)["QQQ"][SoFiHK.PosStock.Stock_CLOSING_PRICE.value]
    """
    print(helpText)

class pdfTable(Enum):
    Table_Portfolio_Summary = 0
    Table_Daily_Trade = 1
    Table_Account_Movement = 2
    Table_Uncleared_Amount = 3
    Table_Pending_Settlement_Transactions = 4
    Table_Stock_Product_Position = 5

class PosStock(Enum):
    Stock_NET_BAL = 0
    Stock_MARKET_VAL = 1
    Stock_PENDING_SETTLE = 2
    Stock_TOTAL_BAL = 3
    Stock_CODE = 4
    Stock_NAME = 5
    Stock_CLOSING_PRICE = 6

class DaySummary(Enum):
    Summary_HKD_Stock = 0
    Summary_HKD_Cash = 1
    Summary_USD_Stock = 2
    Summary_USD_Cash = 3
    Summary_Total_HKD = 4

class DayTrade(Enum):
    Trade_direction = 0
    Trade_stock = 1
    Trade_price = 2
    Trade_share = 3
    Trade_charge = 4
    Trade_total_price = 5
    Trade_stock_code = 6

# Class For init your daily report
class SoFiDReport:
    dict_PORTFOLIO_SUMMARY = {}
    dict_ACCOUNT_MOVEMENT = {}
    dict_Stock_Product_Position = {}

    portfolio_code_list = []

    _pdf = ""
    
    def __init__(self, pathFile):
        with fitz.open(pathFile) as doc:
            text = ""
            for page in doc:
                text += page.getText()
            self._pdf = text
        self._get_code_list()

    def _tripedPortfolioSummary(self):
        self._pdf.split("\n")
        startOfSummary = self._pdf.find("Pending Settlement")
        endOfSummary = self._pdf.find("Cash and Stock Holdings in HKD")
        SummaryTextArea = self._pdf[startOfSummary:endOfSummary]
        SummaryTextList = SummaryTextArea.split("\n")
        result = []
        result.append(SummaryTextList[1]) #Summary_HKD_Stock
        result.append(SummaryTextList[4]) #Summary_HKD_Cash
        result.append(SummaryTextList[6]) #Summary_USD_Stock
        result.append(SummaryTextList[9]) #Summary_USD_Cash
        result.append(SummaryTextList[11]) #Summary_Total_HKD
        return result

    def _tripedDaily_Trade(self):
        self._pdf.split("\n")
        startOfTrade = self._pdf.find("Daily Trades")
        endOfTrade = self._pdf.find("Interest, Pending Settlement And Uncleared Amount")
        TradeTextArea = self._pdf[startOfTrade:endOfTrade]
        tradearealist = TradeTextArea.split("\n")
        tradeIndex = []
        tradeStock = []
        for idx,text  in enumerate(tradearealist):
            if(text == "Buy" or text == "(Internet)" or text == "Sell"):
                tradeIndex.append(idx)
            
        #print(tradeIndex)
        for i in range(0,len(tradeIndex),2):
            start = tradeIndex[i]
            end = tradeIndex[i+1]
            temp = []
            temp.append(tradearealist[start])
            #print(tradearealist[start+2])
            if tradearealist[start+2].replace(".", "").isdigit():
                temp.append(tradearealist[start+1])
                temp.append(tradearealist[start+2])
                temp.append(tradearealist[start+3])
            else:
                offset = 1
                temptext = tradearealist[start+1] + " " + tradearealist[start+2]
                temp.append(temptext)
                temp.append(tradearealist[start+2+offset])
                temp.append(tradearealist[start+3+offset])
                temp.append(tradearealist[end-4])
                temp.append(tradearealist[end-2])
                temp.append(tradearealist[end-1])
                tradeStock.append(temp)
        return tradeStock


    # getProfolio
    _lastValUp = False  # this is the global var for lastValUp
    def _get_code_list(self):
        start = self._pdf.find("Stock/Product Position")
        end = self._pdf.find("* = Product Suspended")
        trippedtxt = self._pdf[start:end]
        test_list = trippedtxt.split("\n")

        # using filter() + lambda 
        # to get string with substring 
        self._lastValUp = False
        def myFilterFunc(x):
            isLength = len(x) < 5 and len(x) > 2
            isUp = x.isupper()
            exceptionList = ["USD"]
            isExcept = x in exceptionList
            isOut = isLength and isUp and not isExcept
            
            # global lastValUp
            if self._lastValUp == False:
                self._lastValUp = isUp
                return isOut
            self._lastValUp = isUp
            return False

        # res = list(filter(lambda x: len(x) < 5 and len(x) > 2 , test_list)) 
        self.portfolio_code_list = list(filter(myFilterFunc , test_list)) 
        
    def _findStock(self, stock):
        start = self._pdf.find("Stock/Product Position")
        end = self._pdf.find("* = Product Suspended")
        trippedtxt = self._pdf[start:end]
        # start = textall.find(stock)
        listText = trippedtxt.split("\n")
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
    
    # ========= For getting Stock Product Position Table =====================
    def _read_portfolio_summary(self):
        return self._tripedPortfolioSummary()


    def _read_Daily_Trade(self):
        return self._tripedDaily_Trade()

    def _read_stock_product_position(self):
        tempdict = {}
        for ticker in self.portfolio_code_list:
            tempdict[ticker] = self._findStock(ticker)
        return tempdict

    def ReadTable(self, enumTable):
        if enumTable == PdfTable.Table_Portfolio_Summary:
            return self._read_portfolio_summary()
        elif enumTable == PdfTable.Table_Daily_Trade:
            return self._read_Daily_Trade()
        elif enumTable == PdfTable.Table_Account_Movement:
            pass
        elif enumTable == PdfTable.Table_Uncleared_Amount:
            pass
        elif enumTable == PdfTable.Table_Pending_Settlement_Transactions:
            pass
        elif enumTable == PdfTable.Table_Stock_Product_Position:
            return self._read_stock_product_position()
            pass
            
