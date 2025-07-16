#!/usr/bin/python3

"""
Translates MTL novels to readable English, and saves final product as epub
"""

import cloudscraper
import requests
from bs4 import BeautifulSoup  # For parsing HTML and XML documents
from ebooklib import epub
import ollama
from PIL import Image
from io import BytesIO
import sys
import uuid
import re
import time
from tqdm import tqdm

scraper = cloudscraper.create_scraper()
delay_overall = 0

# Function to fetch text from a given URL
def fetch_text(url,i):
    #return ['Chapter Title','chapter content','URL of next chapter']
    result = ['','','']
    global delay_overall

    attempt = 1
    base_delay = 1
    while attempt < 6:
        tqdm.write(f'Trying Chapter {i}...')
        try: 
            response = scraper.get(url, timeout=(5, 15))
            if response.status_code == 200:
                page_content = response.content
                soup = BeautifulSoup(page_content, 'html.parser')

                titleelem = soup.find(name='a', class_='chr-title') #find chapter title element
                if titleelem:
                    result[0] = titleelem.get('title')
                else:
                    result[0] = f'Chapter {i}'


                bodyelem = soup.find(name='div', class_='chr-c', id='chr-content')
                if bodyelem:
                    tqdm.write(f'Chapter {i} has been found')
                    inner_html = str(bodyelem)
                    result[1] = inner_html
                else:
                    attempt += 1
                    tqdm.write(f'ALERT ALERT Chapter {i} text has NOT been found, trying attempt {attempt}...')
                    continue

                next_chap_button = soup.find(name='a', id='next_chap', class_='btn btn-success')
                if next_chap_button and not next_chap_button.has_attr("disabled"):        
                    result[2] = next_chap_button.get('href')
                else:
                    result[2] = None 
                    tqdm.write("No next chapter found.")

                return result
            elif response.status_code in (429, 503):
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    delay = int(retry_after)
                    tqdm.write(f"Server asked to retry after {delay} seconds...")
                else:
                    delay = base_delay * (3 ** (attempt - 1))
                    tqdm.write(f"No 'Retry-After' header. Using exponential backoff: {delay} seconds...")

                delay_start = time.time()
                time.sleep(delay)
                delay_end = time.time()
                delay_overall += delay_end-delay_start
                attempt += 1
                tqdm.write(f"Trying attempt {attempt}...")
            else:
                attempt += 1
                tqdm.write(f"The request failed with an error {response.status_code}, retrying immediately")
        except requests.exceptions.Timeout:
            delay = base_delay * (3 ** (attempt - 1))
            tqdm.write(f"Using exponential backoff: {delay} seconds...")
            delay_start = time.time()
            time.sleep(delay)
            delay_end = time.time()
            delay_overall += delay_end-delay_start
            attempt += 1
            tqdm.write(f"Request timed out for URL: {url}")
        except requests.exceptions.RequestException as e:
            delay = base_delay * (3 ** (attempt - 1))
            tqdm.write(f"Using exponential backoff: {delay} seconds...")
            delay_start = time.time()
            time.sleep(delay)
            delay_end = time.time()
            delay_overall += delay_end-delay_start
            attempt += 1
            tqdm.write(f"Request failed: {e}")        
    
    tqdm.write(f"Failed {attempt} attempts, quitting now")
    sys.exit(1)

#Function to clean up the MTL English using an LLM
def grammar_police(contentlist):
    #Bootup Ollama (we are using a locally downloaded deepseek r1 instance with 8b parameters)
    """
    Example:
    response = ollama.chat(
        model='deepseek-r1:8b',
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a novel editor. Your task is to improve the sloppy machine tranlated English "
                    "generated from Chinese text. Make the English natural, fluent, and faithful to the meaning in Chinese. "
                )
            },
            {
                "role": "user",
                "content": (
                    f"Machine Translated English: {content}"
                )
            }
        ]
    )
    """

    return contentlist

# Main function
def main(stop_chapter = float('inf')):
    #-------------- START ---------------
    home_url = input("What's the homepage URL (novelbin): ")
    response = scraper.get(home_url)
    if response.status_code != 200:
        print(f"The request for the URL failed with an error {response.status_code}, {type(response.status_code)}")
        sys.exit(1)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    

    """NEED TO CHECK ALL THE ERROR HANDLING"""
    #Download Some or All Chapters
    stop = input("Do you want a some (Y) or all chapters (N): ")
    if stop == 'Y':
        stop_chapter = int(input("Enter an integer being the number of chapters to download: ")) + 1


    book = epub.EpubBook()

    #-------------- Set Metadata --------------
    book.set_identifier(f"urn:uuid:{uuid.uuid4()}")
    book.set_language('en')

    #-------------- Set Title --------------
    title_elem = soup.find(name='h3', class_='title')
    if title_elem is None:
        ans = input("TITLE NOT FOUND, would you like to manually enter it (Y/N): ")
        if ans == 'y' or ans == 'Y':
            title = input("Enter Book Title: ")
        else:
            print("Quitting...")
            sys.exit(0)
    else:
        book_title = title_elem.text

    book.set_title(book_title) 

    #-------------- Set Cover Image --------------
    img_elem = soup.find(name='img', class_='lazy')
    response = scraper.get(img_elem.get('data-src')) #or 'src' depending on JS utilization
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content)).convert("RGB")
        image = image.resize((400, 600), Image.LANCZOS)

        output = BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)

        book.set_cover('cover.jpg', output.read())
    else:
        print(f"The request for the image failed with an error {response.status_code}")
    
    #-------------- Set Author --------------
    author_elem = soup.find(name='h3', string='Author:').find_next('a')
    book.add_author(author_elem.text)

    #-------------- Build the Chapters --------------
    overall_start = time.time() #Start Overall Timer

    toc = []
    book.spine = ['nav']

    #Find the Latest Chapter for the loading bar
    if not stop == 'Y':
        latest_elem = soup.find(name='div', class_='l-chapter')
        pbar = None
        if latest_elem:
            latest_link_elem = latest_elem.find(name='a', class_='chapter-title')
            if latest_link_elem is None:
                print("Last chapter link was not found, thus loading bar is unavailable")
            else:
                attribute = 'title'
                latest_link = latest_link_elem.get(attribute)
                if latest_link:
                    match = re.search(r'\d+', latest_link)
                    if match:
                        final_chap = int(match.group())
                        pbar = tqdm(total=final_chap)
                    else:
                        print("Last chapter number was not found, thus loading bar is unavailable")
                else:
                    print(f"Latest chapter attribute (\'{attribute}\') not found, what follows is the latest element")
                    print(f"\n\n{latest_elem}")
        else:
            print("Latest element was not found, thus loading bar is unavailable")
    else:
        pbar = tqdm(total=(stop_chapter-1))


    next_chapter = soup.find(name='a', class_='btn-read-now').get('href')
    i = 1
    while not next_chapter is None and i != stop_chapter:
        #-------------- Get Chapter & Next Link --------------
        contentlist = fetch_text(next_chapter,i)
        #contentlist = grammar_police(contentlist)

        #-------------- Create a chapter --------------
        toc.append(epub.Link(f'chap_{i}.xhtml',contentlist[0],f'chapter_{i}'))
        title = contentlist[0]
        content = contentlist[1]
        chapter = epub.EpubHtml(title=title, file_name=f'chap_{i}.xhtml', lang='en')
        chapter.content = f'<div>{content}</div>'
        book.add_item(chapter)
        book.spine.append(chapter)

        i += 1
        if pbar:
            pbar.update(1)
        next_chapter = contentlist[2]

    if pbar:
        pbar.close()


    #-------------- Define Table of Contents --------------
    book.toc = tuple(toc)

    #Add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    #-------------- Define CSS style --------------
    style = 'body { font-family: Times, Times New Roman, serif; }'
    nav_css = epub.EpubItem(uid='style_nav', file_name='style/nav.css', media_type='text/css', content=style)
    book.add_item(nav_css)

    #-------------- Write to file --------------
    bookFile = book_title.replace(' ','_')
    epub.write_epub(f"{bookFile}.epub", book, {})
    
    overall_end = time.time() #End Overall Timer

    print("Mission Complete");

    print(f"\nTotal time taken: {(overall_end-overall_start):.2f} seconds")
    print(f"Time spent on delay: {delay_overall:.2f} seconds")

    print("\n*Remember to move the file from this directory to downloads*")

# Call the main function
if __name__ == "__main__":
    main()
