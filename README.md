![Logo](In_The_Loop/assets/Title_Financial.png)

# In The Loop

Whether you’re just starting off, or are a seasoned trading veteran, In The Loop is a useful tool to gain a quick insight into any publicly traded company, its stock values over the years and some core ratios.

There are three API’s: AlphaVantage, FinancialModelingPrep and NewsAPI. The first two are used to access stock datapoints across the years, company descriptions and other info. Two separate APIs were necessary, given that each one only allows for 5 callbacks/minute. NewsAPI produces the latest news headlines for the stock symbol that the user inputs

Project for my current portfolio. Designed for educational purposes only.
The graphs and charts were built using Dash, by Plotly.
Due to API limitations with the free plan for AlphaVantage and Financial MP, do not run/refresh the app more than once per minute.


## Getting Started

To begin, execute each of the following in your terminal:
```
pip install dash
```
```
pip install dash-bootstrap-components
```
```
pip install pandas
```
```
pip install requests
```

If you prefer Jupyter Notebooks use:
```
pip install jupyter-dash
```


## Authenticating the API

You will need to acquire 3 API tokens to authenticate your access.

---->Set up your personal API key from url = https://www.alphavantage.co/

---->Set up your personal API key from url = https://newsapi.org

---->Set up your personal API key from url = https://financialmodelingprep.com/developer/docs/


## Running the App

In app.py, replace the API key placeholders with your own, personal API keys in their respective categories.
The placeholders can be found directly underneath the import statements on app.py

app.py contains the layout for the dashboard application

You're ready to go! Simply run the code on app.py

In your console, a port address will appear:
```
http://127.0.0.1:8050/
```
Clicking the address will automatically open a new window in your default browser. The placeholder stock symbol is "MSFT", therefore, the stock information for Microsoft should be displaying in your browser window.

## How to use the App
To change which stock you are currently exploring - while the app is still running and your browser window remains open - simply go to your symbol.py folder
and replace "MSFT" with whichever (valid) stock symbol

Return to the open browser window, give it a moment to refresh itself (does it automatically) and voila!

## TroubleShooting
---> The app will only accept valid stock symbols. Crypto info is currently in the works.

---> If your console returns a KeyError, simply wait one full minute and run it again. As mentionned, this is caused
by the limitations set forth by a free API key.

--> In the case of:
      ```
      OSError: [Errno 48] Address already in use
      ```

   Simply add a "port" attribute to the app.run_server
    
```
if __name__ == '__main__':
    app.run_server(debug=True, port=8051) #Or any port > 8050
```
