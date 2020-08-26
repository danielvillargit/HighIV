# HighIV


**High Implied Volatility Options Analytics**


This project takes high implied volatility options data from barchart.com and turns it into actionable trading decisions via technical analysis. The
purpose of this build is to supplement an income trading strategy and automate mundane processes for efficiency. The ultimate goal is to devote more attention
to analysis of potential stock setups rather than searching for good setups hand by hand. 

Selenium is used to download a csv file of potential setups from barchart.com and imported to a pandas dataframe where it is cleaned up. From there, charts
using common technical analysis indicators are generated for each ticker using Tradingview. Option chain information is imported via the TDAmeritradeAPI where
all out of the money strikes are stored as a Dataframe. Requests are limited to 50 per minute to underload the maximum requests allowed by a TD Developer account.


**Upcoming Release**


The next major release of this package will include taking the data and graphs from this project and creating a static dynamic web page using Django.
The idea is to create a clean UI that shows all information gathered by class OptionSearch for each ticker individually.


| Option Search Functions | Description |
|---------------------------|---------------------------|
|     **BarchartImport**                   |      Downloads csv file from barchart.com             |
|     **OptionImport**                   |      Compiles information from barchart csv file and does basic datacleanup            |
|     **TChart**                   |      Saves screenshot of tickers with technical indicators from Tradingview's interactive chart            |
|     **GetEarnings**                   |      Scrapes beta and earnings data form finviz.com             |
|     **AmerConnect**                   |      Requests Option Chains from TDAmeritradeAPI            |



