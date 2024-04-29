from subprocess import getstatusoutput
from time import sleep


while True:
    InternetStatus = int((getstatusoutput('ping -n 2 www.youtube.com >nul && echo 0 || echo 1'))[1])

    if InternetStatus == 0:

        import pymongo
        import requests
        from bs4 import BeautifulSoup
        from tabulate import tabulate
        from datetime import datetime, timedelta
        import pyotp
        from time import sleep, time
        from SmartApi.smartConnect import SmartConnect
        import math

        # "₹ " +




        while True:
            try:
                available_balance = int(input("Enter Balance ₹ : "))
                break
            except:
                print("Type in Numbers")
                continue
        a = time()

        PotentialDividendSum = []

        DividendCompanies = []

        DividendActive = 0
        DividendInactive = 0

        DividendActiveAmount = []
        DividendInactiveAmount = []

        Databases = ['AlgoTrading', 'SmartAPI']
        collections = ['NSE_Tickers', 'Angelone Credentials']

        # Function to fetch current price using SmartAPI


        def bordered(text):
            lines = text.splitlines()
            width = max(len(s) for s in lines)
            res = ['┌' + '─' * width + '┐']
            for s in lines:
                res.append('│' + (s + ' ' * width)[:width] + '│')
            res.append('└' + '─' * width + '┘')
            return '\n'.join(res)



        def get_current_price(obj, exchange, symbol, token):
            try:
                ltp_data = obj.ltpData(exchange, symbol, token)
                current_price = ltp_data['data']['ltp']
                sleep(0.10)
                return current_price
            except Exception as e:
                # print(f"Historic Api failed: {e}")
                return "N/A"


        # Function to get dividend status (Active/Inactive)
        def get_dividend_status(ex_dividend_date, buffer_days=1):
            try:
                # Parse the date string
                ex_date = datetime.strptime(ex_dividend_date, '%b %d, %Y').date()

                # Get today's date
                today = datetime.today().date()

                # Consider a buffer period before the record date
                buffer_period = timedelta(days=buffer_days)
                record_date = ex_date - buffer_period

                # Compare dates to determine dividend status
                if record_date >= today:
                    return "Active"
                else:
                    return "Inactive"
            except Exception as e:
                # Handle any exceptions (e.g., invalid date format)
                print(f"Error in get_dividend_status: {e}")
                return "N/A"


        # Credentials and setup for SmartAPI
        def Downloader(database, collection, filter_name):
            client = pymongo.MongoClient(
                "mongodb+srv://SupremeRahul:XSQ7yAJVndHtznuj@clusternse.wpf8cel.mongodb.net/?retryWrites=true&w=majority")
            db = client[database][collection].find({"name": filter_name}, {"_id": 0})

            for i in db:
                return i

        Credentials = Downloader(Databases[1],collections[1], "Shubham Morkhade")


        obj = SmartConnect(api_key=Credentials['apikey'])
        data = obj.generateSession(Credentials['username'], Credentials['password'], pyotp.TOTP(Credentials['totp']).now())
        refreshToken = data['data']['refreshToken']
        feedToken = obj.getfeedToken()


        def NSE_Tickers():
            client = pymongo.MongoClient(
                "mongodb+srv://SupremeRahul:XSQ7yAJVndHtznuj@clusternse.wpf8cel.mongodb.net/?retryWrites=true&w=majority")
            db = client['AlgoTrading']['NSE_Tickers']
            array = []
            for i in db.find({}, {"_id": 0}):
                array.append(i)

            return array

        print("Wait...We are computing data for you 😄\n\n")

        nse_data = NSE_Tickers()

        # Create a dictionary to map symbols to tokens
        symbol_to_token = {entry['symbol']: entry['token'] for entry in nse_data}

        # URL to fetch dividend data
        url = 'https://www.chittorgarh.com/report/stock-dividend/135/'

        # Fetch HTML data from the URL
        response = requests.get(url)
        html_table_data = response.text

        # Parse HTML table data
        soup = BeautifulSoup(html_table_data, 'html.parser')

        # Find all rows in the table
        rows = soup.find_all('tr')

        # Extract and display information in tabular format
        data = []
        header = ["Company Name", "Stock Symbol", "Ex-Date", "Dividend Status", "Dividend Amount", "Current Price", "Qty",
                  "Potential Dividend", "Invest Amount"]

        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 8:
                company_name_tag = columns[0].find('a')
                company_name = company_name_tag.get_text(strip=True) if company_name_tag else ''
                company_name = company_name.replace('-$', '')

                stock_symbol = columns[1].get_text(strip=True) + "-EQ"
                stock_code = columns[2].get_text(strip=True)

                symbol_token = symbol_to_token.get(stock_symbol, 'N/A')

                ex_dividend_date = columns[3].get_text(strip=True)
                dividend_amount = columns[6].get_text(strip=True)

                current_price = get_current_price(obj, 'NSE', stock_symbol, symbol_token)
                dividend_status = get_dividend_status(ex_dividend_date)








                if current_price != "N/A":
                    DividendCompanies.append(company_name)
                    Quantity = math.modf(available_balance / float(current_price))[1]
                    PotentialDividend = Quantity * float(dividend_amount)
                    PotentialDividendSum.append(PotentialDividend)
                    InvestableAmount = float(current_price) * Quantity

                    rounded_number = round(InvestableAmount, 2)
                    InvestAmount = str("{:.2f}".format(rounded_number)) + "/-"

                    rounded_number1 = round(PotentialDividend, 2)
                    PotentialDividend = str("{:.2f}".format(rounded_number1)) + "/-"


                    if dividend_status == "Active":
                        DividendActive += 1
                        DividendActiveAmount.append(float(dividend_amount) * float(Quantity))
                    else:
                        DividendInactive += 1
                        DividendInactiveAmount.append(float(dividend_amount) * float(Quantity))

                    data.append([company_name, stock_symbol, ex_dividend_date, dividend_status, dividend_amount, current_price,
                                 Quantity, PotentialDividend, InvestAmount])




        # Print the table using tabulate
        table = tabulate(data, headers=header, tablefmt="pretty")
        print(table)

        TotalDividend = sum(PotentialDividendSum)


        print("\n")
        print("=" * 110)
        print(f"Total Potential Dividend Can be Earned is: Rs. {str(TotalDividend) + '/-'} \n")
        print(f"Your Return of Dividend on Investment of Rs. {available_balance} is {(str((TotalDividend / available_balance) * 100))[0:5]}%")

        print("=" * 110)

        print(f"Total {len(DividendCompanies)} Companies providing Dividend")

        Dividend_Earn_able = (sum(float(amount) for amount in DividendActiveAmount))

        rounded_number = round(Dividend_Earn_able, 2)
        Earn_Dividend_Still = str("{:.2f}".format(rounded_number)) + "/-"
        borderData = (f"\n{DividendActive} / {DividendInactive} Dividend Active Yet\n"
                      "--------------------------------------------------\n"
                      f"From Rs. {available_balance}..."
                      f"\nDividends You can Earn Still : {Earn_Dividend_Still}  \n"
        
                      f"\nEarn-able Dividend You Missed Yet : {str(sum(float(amount) for amount in DividendInactiveAmount)) + '/-'}")

        print(bordered(borderData))


        b = time()
        print(f"Feed Ready in {(str(b - a))[0:6]}'s ")
        break
    else:
        print("Connect to Internet, and Restart the Program")
        sleep(5)




while True:
    inp = input('Enter Y to exit (else ignore)')
    if "Y" or 'y' in inp:

        quit()
    else:
        continue