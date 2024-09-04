from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib3.exceptions import InsecureRequestWarning
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, String, BigInteger, Numeric, Integer, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric
from datetime import datetime
import chromedriver_autoinstaller, re, os, time, requests, warnings, sys

warnings.filterwarnings("ignore", category=InsecureRequestWarning)
warnings.filterwarnings("ignore", category=ResourceWarning)
warnings.filterwarnings("ignore", message="Connection pool is full, discarding connection")

LOCK = 0
KILL = 0

# Database URL
DATABASE_URL = "postgresql+psycopg2://postgres:root@db/crypto"

# Create an engine
engine = create_engine(DATABASE_URL)

Base = declarative_base()
# Create tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

class Cryptocurrency(Base):
    __tablename__ = 'cryptocurrency'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    price = Column(Numeric(18, 4))  # Precision of 18 and scale of 4
    price_change = Column(Numeric(18, 2))  # Precision of 18 and scale of 2
    volume = Column(Numeric(18, 2))  # Precision of 18 and scale of 2
    vol_change = Column(Numeric(18, 2))  # Precision of 18 and scale of 2
    vol_rank = Column(Integer)
    circulating_supply = Column(BigInteger)
    total_supply = Column(BigInteger)
    max_supply = Column(BigInteger)
    diluted_market_cap = Column(Numeric(18, 2))  # Precision of 18 and scale of 2
    contracts = Column(JSON)
    socials = Column(JSON)
    official_links = Column(JSON)
    last_update = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    

TOP100 = ['bitcoin', 'ethereum', 'tether', 'bnb', 'solana', 'usd-coin', 'xrp', 'dogecoin', 'tron', 'toncoin', 'cardano', 'avalanche', 'shiba-inu',
        'chainlink', 'polkadot-new', 'bitcoin-cash', 'near-protocol', 'unus-sed-leo', 'multi-collateral-dai', 'polygon', 'litecoin', 'kaspa',
        'internet-computer', 'uniswap', 'pepe', 'artificial-superintelligence-alliance', 'aptos', 'first-digital-usd', 'monero', 'ethereum-classic',
        'stellar', 'stacks', 'bittensor', 'render', 'sui', 'immutable-x', 'filecoin', 'okb', 'cronos', 'injective', 'mantle', 'hedera', 'arbitrum',
        'vechain', 'maker', 'cosmos', 'aave', 'dogwifhat', 'optimism-ethereum', 'arweave', 'the-graph', 'floki-inu', 'thorchain', 'fantom', 'bonk1',
        'bitget-token-new', 'theta-network', 'jupiter-ag', 'celestia', 'helium', 'sei', 'algorand', 'pyth-network', 'lido-dao', 'jasmy', 'core-dao',
        'paypal-usd', 'kucoin-token', 'ondo-finance', 'flow', 'notcoin', 'bitcoin-sv', 'based-brett', 'bittorrent-new', 'multiversx-egld', 'quant',
        'eos', 'mantra', 'onbeam', 'sats', 'akash-network', 'usdd', 'axie-infinity', 'neo', 'gala', 'popcat-sol', 'tezos', 'ordi', 'gatetoken',
        'ethereum-name-service', 'dydx-chain', 'flare', 'klaytn', 'ecash', 'dogs', 'worldcoin-org', 'the-sandbox', 'conflux-network', 'starknet-token', 'wormhole']

class CoinMarketCap:
    
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("disable-gpu")
        self.option.add_argument('--headless=new')
        self.option.add_argument('--no-sandbox')
        # self.option.add_argument('--disable-dev-sh-usage')
        self.option.add_argument('--shm-size=1gb')
        self.option.add_argument('--blink-settings=imagesEnabled=false')
        self.option.add_argument("--log-level=3")
        self.option.add_experimental_option('excludeSwitches', ['enable-logging'])

        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome(options=self.option)

    def getData(self, name):
        self.driver.get(f'https://coinmarketcap.com/currencies/{name}/')
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        error_tag = self.soup.find('p', string=re.compile("Sorry"))

        if error_tag:
            return {'error': 'Coin not Found'}
        
        def getMetrics():
            dl_element = self.soup.find('dl', class_='coin-metrics-table')
            metrics_values = {}
            metric_mapping = {
                'Market cap': 'market_cap',
                'Volume (24h)': 'volume',
                'Volume/Market cap (24h)': 'volume_change',
                'Circulating supply': 'circulating_supply',
                'Total supply': 'total_supply',
                'Max. supply': 'max_supply',
                'Fully diluted market cap': 'diluted_market_cap'
            }

            for child in dl_element.children:
                if child.name == 'div':
                    dt_element = child.find('dt')
                    dd_element = child.find('dd')
                    if dt_element and dd_element:
                        metric_name = dt_element.find('div').text.strip()
                        metric_value = dd_element.get_text(strip=True).replace('(1d)', '')
                        rank_value_span = child.find('span', class_='rank-value')
                        rank_value = rank_value_span.get_text(strip=True).replace('(1d)', '') if rank_value_span else None
                        
                        if metric_name in metric_mapping:
                            key = metric_mapping[metric_name]
                            if key == 'volume_change':
                                match = re.search(r'([\d.]+%)', metric_value)
                                if match:
                                    volume_change = float(match.group(1).strip('%').replace('(1d)', ''))
                                    change_direction = dd_element.find('p', attrs={'data-change': True})
                                    if change_direction and change_direction['data-change'] == 'down':
                                        volume_change *= -1
                                    metrics_values[key] = volume_change
                                else:
                                    metrics_values[key] = None
                            else:
                                match = re.search(r'([\d,.]+)', metric_value)
                                value = match.group(1).replace(',', '').replace('(1d)', '') if match else None
                                if value:
                                    metrics_values[key] = float(value) if '.' in value else int(value)
                                else:
                                    metrics_values[key] = None
                                    
                            if rank_value is not None:
                                metrics_values[f'{key}_rank'] = int(re.search(r'\d+', rank_value).group()) if rank_value else None
            
            output = {
                "symbol": list(self.soup.find('div', class_='coin-symbol-wrapper').children)[0].text,
                "price": None,
                "price_change": None,
                "market_cap": metrics_values.get("market_cap"),
                "market_cap_rank": metrics_values.get("market_cap_rank"),
                "volume": metrics_values.get("volume"),
                "volume_rank": metrics_values.get("volume_rank"),
                "volume_change": metrics_values.get("volume_change"),
                "circulating_supply": metrics_values.get("circulating_supply"),
                "total_supply": metrics_values.get("total_supply"),
                "max_supply": metrics_values.get("max_supply"),
                "diluted_market_cap": metrics_values.get("diluted_market_cap"),
            }

            return output

        def getSocials():
            coin_info_links = self.soup.find('div', class_='coin-info-links')
            social_links = coin_info_links.find_all('a', href=True)
            official_links = []
            socials = []
            
            for link in social_links:
                url = link['href']
                text = link.get_text(strip=True)
                if "0x" in text:
                    continue
                
                link_data = {'name': text.lower(), 'url': url}
                if text.lower() == 'website':
                    official_links.append({'name': 'website', 'link': url})
                else:
                    socials.append(link_data)

            contract_element = self.soup.find('a', class_='chain-name')
            try:
                contract_name = contract_element.get_text(strip=True)
                contract_url = contract_element['href']
                contract_address = contract_url.split('/')[-1]
            except (AttributeError, KeyError):
                contract_name = None
                contract_address = None
                
            output = {
                "contracts": [{
                    'name': contract_name,
                    'address': contract_address
                }],
                'official_links': official_links,
                'socials': socials
            }
            return output

        def getPrice():
            price_div = self.soup.find('div', {'data-role': 'el'}).find_next('div', {'data-role': 'el'})
            price_span = price_div.find('span')
            price_text = price_span.get_text(strip=True).replace('(1d)', '') if price_span else "N/A"

            percentage_change_div = price_div.find_next('div')
            percentage_change_p = percentage_change_div.find('p') if percentage_change_div else None
            percentage_change_text = percentage_change_p.get_text(strip=True).replace('(1d)', '') if percentage_change_p else "N/A"
            change_direction = percentage_change_p['data-change'] if percentage_change_p and 'data-change' in percentage_change_p.attrs else None

            price = float(price_text.replace('$', '').replace(',', '').replace('(1d)', '')) if price_text != "N/A" else None
            percentage_change = float(percentage_change_text.replace('%', '').replace('\xa0(1d)', '').replace('(1d)', '')) if percentage_change_text != "N/A" else None

            if change_direction == 'down':
                percentage_change *= -1

            output = {
                "price": price,
                "price_change": percentage_change
            }

            return output
        
        with ThreadPoolExecutor(max_workers=16) as executor:
            future_to_function = {
                executor.submit(getPrice) : 'price',
                executor.submit(getMetrics) : 'metrics',
                executor.submit(getSocials) : 'socials',
            }
            results = {}
            for future in as_completed(future_to_function):
                func_name = future_to_function[future]
                
                try:
                    results[func_name] = future.result()
                except Exception as e:
                    results[func_name] = f'Generated an exception: {e}'
        # data = (getPrice(), getMetrics(), getSocials())
        
        # x = data[1]
        # x['price'] = data[0]['price']
        # x['price_change'] = data[0]['price_change']
        # x['contracts'] = data[2]['contracts']
        # x['official_links'] = data[2]['official_links']
        # x['socials'] = data[2]['socials']
        
        # return x
        
        data = results['metrics']
        data['name'] = name
        data['price'] = results['price'].get('price')
        data['price_change'] = results['price'].get('price_change')
        data['contracts'] = results['socials'].get('contracts')
        data['official_links'] = results['socials'].get('official_links')
        data['socials'] = results['socials'].get('socials')

        return data

    def closeDriver(self):
        if self.driver:
            self.driver.close()
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeDriver()

def check_killswitch():
    
    global KILL
    
    with open('ops.dat', 'r+') as file:
        content = file.read()
        if content:
            data = content.strip().split(',')
            if len(data) < 2:
                if 'killswitch' in data:
                    file.seek(0)
                    file.truncate(0)
                    print('Close scrapper command initiated')
                    KILL = 1
                    return True
                else: return False
        return False


def get_top_100_coins():
    
    url = "https://coinmarketcap.com/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table with the class 'cmc-table'
    table = soup.find('table', class_='cmc-table')

    coin_names = []

    for row in table.find_all('tr')[1:101]:  # Skipping the header row
        # Find the 'a' tag with the href attribute in each row
        link = row.find('a', href=True)
        if link:
            # Extract the last part of the href (coin name)
            coin_name = link['href'].split('/')[-2]
            coin_names.append(coin_name)

    # print(coin_names)
    return coin_names

def start_DB_service(delay, batch):

    global LOCK
    print("Currently running on 5 Minute interval")
    
    while not KILL:
        try:
            if check_killswitch():
                while LOCK:
                    print("Lock not Released..")
                    time.sleep(1)
                break 
            scrape_latest_coin_data(batch)
            # print("now here")
            
        except Exception as e:
            print(f"An error occurred: {e}")
        
        # Wait for the specified interval before reading again
        print(f"{delay} seconds Timeout : {datetime.now().time()}")
        time.sleep(delay)


def scrape_latest_coin_data(batch=10):
    
    global TOP100
    
    BATCH_SIZE = batch
    output = {}
    
    for i in range(0, len(TOP100), BATCH_SIZE):
        batch = TOP100[i:i + BATCH_SIZE]
        print(f"Processing batch {i // BATCH_SIZE + 1} of {len(TOP100) // BATCH_SIZE}")
        
        if check_killswitch(): break
        
        try:
            with CoinMarketCap() as cm:
                for coin in batch:
                    try:
                        print(f"Fetching data for {coin}...")
                        data = cm.getData(coin)
                        output[coin] = data
                        # print(data)
                        
                    except Exception as e:
                        print(f"Error fetching data for {coin}: {e}")
            
            insert_coin_data(output)
            #call DB function here
        except Exception as e:
            print(f"error occured : {e}")

    return output


def start_scrapper():
    scrape_latest_coin_data()
    

def insert_coin_data(coins):
    
    global LOCK
    
    LOCK = 1
    for coin_data in coins:
        
        coin_dict = {
            'id': f"{coins[coin_data].get('name')}-{coins[coin_data].get('symbol')}", 
            'name': coins[coin_data].get('name'),
            'symbol': coins[coin_data].get('symbol'),
            'price': coins[coin_data].get('price'),
            'price_change': coins[coin_data].get('price_change'),
            'volume': coins[coin_data].get('volume'),
            'vol_change': coins[coin_data].get('volume_change'),
            'vol_rank': coins[coin_data].get('volume_rank'),
            'circulating_supply': coins[coin_data].get('circulating_supply'),
            'total_supply': coins[coin_data].get('total_supply'),
            'max_supply': coins[coin_data].get('max_supply'),
            'diluted_market_cap': coins[coin_data].get('diluted_market_cap'),
            'contracts': coins[coin_data].get('contracts'),
            'socials': coins[coin_data].get('socials'),
            'official_links': coins[coin_data].get('official_links'),
            'last_update': datetime.utcnow()
        }
        
        try:
            insert_stmt = insert(Cryptocurrency).values(coin_dict)
            
            # Define the on_conflict_do_update statement, excluding only 'id' and 'name'
            do_update_stmt = insert_stmt.on_conflict_do_update(
                index_elements=['id'], #unique constraint
                set_={key: getattr(insert_stmt.excluded, key) for key in coin_dict.keys() if key not in ['id', 'name']}
            )
            
            # Execute the statement and commit the transaction
            session.execute(do_update_stmt)
            session.commit()
            print(f"Inserted/Updated {coin_dict['name']} values.")
        
        except Exception as e:
            session.rollback()  # Rollback in case of error
            print(f"Error Updating data for {coin_dict['name']}: {e}")
    
    LOCK = 0

if __name__ == '__main__':
    
    if not os.path.exists('ops.dat'): 
        with open('ops.dat', 'w') as file: 
            pass
    
    b = 10
    if sys.argv[-1]:
        b = int(sys.argv[-1])
    start_DB_service(300, b)
    print('Service Ended.')
    
