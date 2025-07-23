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

#Custom Created Packages
from processors.novelbin import NovelBin
from processors.royalroad import RoyalRoad

scraper = cloudscraper.create_scraper()
delay_overall = 0

# Function to fetch text from a given URL
def fetch_text(url,i,website):
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

                """TODO: Check if title is in first line, else add it to body text"""
                result[0] = website.find_chapter_title(soup, i)


                body_text = website.find_chapter_text(soup)
                if body_text:
                    tqdm.write(f'Chapter {i} has been found')
                    result[1] = body_text
                else:
                    attempt += 1
                    tqdm.write(f'ALERT ALERT Chapter {i} text has NOT been found, trying attempt {attempt}...')
                    continue

                
                next_chapter_link = website.find_next_chapter(soup)
                result[2] = next_chapter_link
                if next_chapter_link == None:
                    tqdm.write("No next chapter found.")
                
            
                """
                TODO: Test of the Royal Road Upheaval Next Chapter Button
                """

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
    #Check if in Royalroad or NovelBin Mode
    mode = None
    for arg in sys.argv:
        mode = arg

    match mode:
        case "-rr":
            website = RoyalRoad('RoyalRoad') 
        case "-nbin":
            website = NovelBin('Novel Bin')

        case _:
            print("\nPass the mode that you would like to use ('rr' or 'nbin') as a part of your call, like so")
            print("=" * 60)
            print("python MTLTranslator.py -rr")
            print("=" * 60, end='\n\n')
            sys.exit(1)  

    #-------------- START ---------------
    home_url = input(f"What's the homepage URL ({website.domain_name}): ")
    website.base_url = home_url
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

    #-------------- Set Metadata --------------
    book = epub.EpubBook()
    book.set_identifier(f"urn:uuid:{uuid.uuid4()}")
    book.set_language('en')

    #-------------- Set Title --------------

    book_title = website.find_title(soup=soup)
    book.set_title(book_title) 

    #-------------- Set Cover Image --------------

    img_link = website.find_cover_image(soup)
    response = scraper.get(img_link)
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
        
    author = website.find_author_name(soup)
    book.add_author(author)

    #-------------- Build the Chapters --------------
    overall_start = time.time() #Start Overall Timer

    toc = []
    book.spine = ['nav']
    """TODO: Latest Chapter for RoyalRoad PBar Number"""
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


    next_chapter = website.find_first_read(soup=soup)
    i = 1
    while not next_chapter is None and i != stop_chapter:
        #-------------- Get Chapter & Next Link --------------
        """TODO: CHANGE FETCH_TEXT TO BE WEBSITE SPECIFIC"""
        contentlist = fetch_text(next_chapter,i,website)
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

    print("Mission Complete")

    print(f"\nTotal time taken: {(overall_end-overall_start):.2f} seconds")
    print(f"Time spent on delay: {delay_overall:.2f} seconds")

    print("\n*Remember to move the file from this directory to downloads*")

# Call the main function
if __name__ == "__main__":
    main()
