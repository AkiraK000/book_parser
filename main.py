import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
import csv
import json

def get_html(url):
    headers = {
        "User-Agent":"Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        return response.text
    else:
        print("Ошибка запроса страницы")
        return ""

html = get_html('https://www.labirint.ru/best/')

soup = BeautifulSoup(html, 'html.parser')
books = soup.find_all("div", class_='product')
console = Console()
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Название", style="dim")
table.add_column("Автор", style="dim")
table.add_column("Цена со скидкой", style="green")
table.add_column("Цена без скидки", style="red")

book_data = []

for book in books:
    title = book.find("span", class_="product-title")
    author = book.find("div", class_="product-author")
    current_price = book.find("span", class_="price-val")
    old_price = book.find("span", class_="price-old")

    title_print = title.text.strip() if title else "N/A"
    author_print = author.text.strip() if author else "N/A"
    current_price_print = current_price.text.strip() if current_price else "N/A"
    old_price_print = old_price.text.strip() if old_price else "N/A"

    if title_print != "N/A":
        book_data.append({
            "title": title_print,
            "author": author_print,
            "price": current_price_print,
            "old_price": old_price_print
        })
        table.add_row(title_print, author_print, current_price_print, old_price_print)
        table.add_row("[dim]" + "─" * 20, "─" * 20, "─" * 20, "─" * 20)

console.print(table)

def save_to_csv(books):
    with open("books.csv", "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["title", "author", "price", "old_price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(book)

def save_to_json(books):
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def save_to_txt(books):
    with open("books.txt", "w", encoding="utf-8") as f:
        for book in books:
            f.write(f"{book['title']} — {book['author']}\n")
            f.write(f"Цена: {book['price']} (Была: {book['old_price']})\n\n")

save_to_csv(book_data)
save_to_json(book_data)
save_to_txt(book_data)