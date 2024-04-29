# DividendROI-Calculator


**DividendTracker** is a Python script designed to help investors analyze potential dividend earnings from listed companies on the National Stock Exchange (NSE) of India. It utilizes data from the NSE and Angel One API to fetch information about dividend-paying companies, their current prices, and dividend amounts. The script calculates the potential dividend earnings based on the user's available balance and provides insights into active and inactive dividend opportunities.

## Features:

- Fetches current stock prices using the Angel One API.
- Determines the dividend status (active or inactive) based on ex-dividend dates.
- Calculates potential dividend earnings for each company.
- Provides a summary of total potential dividend earnings and dividend opportunities.
- Offers insights into missed dividend opportunities and remaining earnable dividends.

## How to Use:

1. **Clone the repository** to your local machine.
2. **Install the required dependencies** listed in `requirements.txt`.
3. **Update the MongoDB connection details and API credentials** in the script.
4. **Run the script** and enter your available balance when prompted.
5. **View the generated table** with dividend information and earnings potential.

## Dependencies:

- Python 3.x
- pymongo
- requests
- BeautifulSoup (bs4)
- tabulate
- pyotp
- SmartApi

## Contribution Guidelines:

Contributions to **DividendTracker** are welcome! If you find any bugs, have feature requests, or want to contribute enhancements, please follow these steps:

1. **Fork the repository**.
2. Create a new branch for your changes (`git checkout -b feature/new-feature`).
3. **Make your changes** and commit them (`git commit -am 'Add new feature'`).
4. **Push your changes** to your fork (`git push origin feature/new-feature`).
5. **Submit a pull request** with a detailed description of your changes.

## License:

This project is licensed under the [MIT License](LICENSE).
