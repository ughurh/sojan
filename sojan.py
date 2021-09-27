from bs4 import BeautifulSoup
import requests
import logging

logging.basicConfig(
    filename='sojan.log', 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.DEBUG)

HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Accept-Language' : 'en-US,en;q=0.9,*;q=0.5'
}

URL_TEMPLATE = 'https://stackoverflow.com/jobs?pg='
page_curr = 1
page_end = False
data ={}

while not page_end:
    page_next = f'{URL_TEMPLATE}{page_curr}'
    response = requests.get(page_next, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = soup.find_all(class_='js-result')

    if not jobs:
        page_end = True
    else:
        logging.debug('Parsing page ' + str(page_curr))
        print('Parsing page ' + str(page_curr))
        for job in jobs:
            logging.debug(job.find_all('a')[1].text)  # get and log job title
            tag_links = job.find_all('a')[2:]  # skip first two nontag links
            for tag in tag_links:
                logging.debug(tag.text)
                data[tag.text] = data.get(tag.text, 0) + 1
            logging.debug('---') 
        page_curr+=1
    
logging.debug('Total tags: ' + str(len(data)))
print('\nTotal tags: ' + str(len(data)))

TOP_N = 15
data = sorted(data.items(), key=lambda item: item[1], reverse=True)
logging.debug('Top tags: ' + str(data[:TOP_N]))

print(f'\nTop {TOP_N} tags:')
print('---')
for item in data[:TOP_N]:
    print(item[0], '-', item[1])
