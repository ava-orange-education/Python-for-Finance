
from plotnine import ggplot, aes, geom_line
import numpy as np
import pandas as pd
import yfinance as yahf
import datetime
import logging


class MovingAverageStockPrice:
  
  
      def __init__(self):
          self.name = "MovingAveragePrice"
          self.data = None
          self.dataset_index = 0

          
      def getMovingAverage(self,prices,window1,window2,period):
	      prices['first']=prices['Close'].rolling(window=window1,min_periods=period,center=False).mean()
	      prices['second']=prices['Close'].rolling(window=window1,min_periods=period,center=False).mean()
    
	      return prices
        
      def getStockPricePositions(self,data,window1,window2,period):
          
          prices = self.getMovingAverage(data,window1,window2,period)
          
          prices['positions'] = 0
          
          prices['positions'][window1:]=np.where(prices['first'][window1:]>=prices['second'][window1:],1,0)

          prices['prices']=prices['positions'].diff()

          prices['oscillator']=prices['first']-prices['second']

          return prices

      def createPlot(self,prices, stockSymbol):

       
          
          fig = (ggplot(prices)  + aes(x="Volume", y="Close") + geom_line())
         
          fig.save("plot.png")

          #fig.show()

          


      def getStockPrices(self,stockSymbol,range_start,range_end):
        
          print("getting stock price")
          data=yahf.download(stockSymbol,start=range_start,end=range_end)
          
          #data = yahf.download(stockSymbol,period="1mo")
          
          #data = yahf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")
          
          print("data",data)
          
          return data

def main():
    logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.INFO)
    logging.getLogger("finance").setLevel(logging.INFO)
    priceIndicator = MovingAverageStockPrice()
    #start_date = datetime.date(2012,10,21)
    #end_date = datetime.date(2013,1,27)
    #stock_symbol = "BA"
    
    start_date = datetime.date(2023,6,21)
    end_date = datetime.date(2023,8,9)
    stock_symbol = "MSFT"
    period=1
    data = priceIndicator.getStockPrices(stock_symbol,start_date,end_date)
    print("stock data",data)
    #window1 = 12
    #window2 = 26
    
    window1 = 10
    window2 = 18
    positions = priceIndicator.getStockPricePositions(data,window1,window2,period)
    priceIndicator.createPlot(positions,stock_symbol)

if __name__ == '__main__':
    main()