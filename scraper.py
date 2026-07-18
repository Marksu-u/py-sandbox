import requests
from bs4 import BeautifulSoup
import csv

def scrape_books():
    url = "https://books.toscrape.com/"
    
    print(f"Fetching data from {url}...\n")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    books = soup.find_all('article', class_='product_pod')
    print(f"Found {len(books)} books on the homepage!\n")
    
    scraped_data = []
    
    for book in books:
        title = book.find('h3').find('a')['title']
        
        price = book.find('p', class_='price_color').text
        
        print(f"Title: {title}")
        print(f"Price: {price}")
        print("-" * 40)
        
        scraped_data.append([title, price])
        
    csv_filename = 'books.csv'
    print(f"\nSaving this data to {csv_filename}...")
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price'])
        writer.writerows(scraped_data)
        
    print("Done! You have successfully scraped the web.")

if __name__ == "__main__":
    scrape_books()
