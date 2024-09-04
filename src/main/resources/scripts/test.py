import requests
from bs4 import BeautifulSoup

url = "https://coinmarketcap.com/bitcoin"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Find the table with the class 'cmc-table'
print(list(soup.find('div', class_='coin-symbol-wrapper').children)[0].text)

# for x in div.children:
#     print(x.text)


# import time

# def read_and_clear_file():
#     while True:
#         try:
#             with open('test.dat', 'r+') as file:
#                 content = file.read()
#                 if content:
#                     data = content.strip().split(',')
#                     if len(data) < 2:
#                         if 'killswitch' in data:
#                             file.seek(0)
#                             file.truncate(0)
#                             break 
                        
#                     print(data)
#                     file.seek(0)  # Move to the beginning of the file
#                     file.truncate(0)  # Clear the file content
#         except Exception as e:
#             print(f"An error occurred: {e}")
        
#         # Wait for the specified interval before reading again
#         time.sleep(3)

# if __name__ == "__main__":
#     read_and_clear_file()
