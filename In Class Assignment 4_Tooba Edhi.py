import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick # optional may be helpful for plotting percentage
import numpy as np
import pandas as pd
import seaborn as sb # optional to set plot theme
import yfinance as yf
sb.set_theme() # optional to set plot theme

DEFAULT_START = dt.date.isoformat(dt.date.today() - dt.timedelta(365))
DEFAULT_END = dt.date.isoformat(dt.date.today())

class Stock:
    def __init__(self, symbol, start=DEFAULT_START, end=DEFAULT_END):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = self.get_data()


    def get_data(self):
        """method that downloads data and stores in a DataFrame"""
        df = yf.download(self.symbol, start=self.start, end=self.end, progress=False)
        df.index = pd.to_datetime(df.index, errors="ignore") #I used ChatGPT to add the "error" element to my code.
        df.index.name = "Date"
        self.calc_returns(df)
        self.data = df
        return df

    
    def calc_returns(self, df):
        """Add relative close to change and daily log (instantaneous) return."""
        close = df["Close"]
        df["change"] = close.pct_change().round(4)
        df["instant_return"] = np.log(close).diff().round(4)
        return df


    def plot_return_dist(self):
        """Plot histogram of instantaneous (log) returns."""
        r = self.data["instant_return"].dropna()
        plt.hist(r, bins=35, density=True, edgecolor='w')
        plt.title(f"{self.symbol} Daily Log Return Distribution")
        plt.show()


    def plot_performance(self):
        """Plot % gain/loss of the stock over time."""
        close = self.data["Close"].dropna()
        perf = close / close.iloc[0] - 1
        plt.plot(perf)
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
        plt.title(f"{self.symbol} Performance")
        plt.show() # I used ChatGPT to help me plot this gain/loss of stock over time. My code had errors and I couldn't
                   # fix it.

def main():
    test = Stock("AAPL")
    print(test.data.head())
    test.plot_performance()
    test.plot_return_dist()


if __name__ == '__main__':
    main() 