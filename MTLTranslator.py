#!/usr/bin/python3

"""
Translates MTL novels to readable English, and saves final product as epub
"""

import requests  # For sending HTTP requests and receiving HTTP responses
from bs4 import BeautifulSoup  # For parsing HTML and XML documents
from ebooklib import epub
import ollama
import sys
import uuid


# Function to fetch text from a given URL
def fetch_text(url,i):
    #return ['Chapter Title','chapter content','URL of next chapter']
    result = ['','','']

    attempt = 0
    while attempt < 5:
        print(f'Trying Chapter {i}...')
        response = requests.get(url)
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
                print(f'Chapter {i} has been found')
                inner_html = str(bodyelem)
                result[1] = inner_html
            else:
                print(f'ALERT ALERT Chapter {i} text has NOT been found')
                continue

            next_chap_button = soup.find(name='a', id='next_chap', class_='btn btn-success')
            if next_chap_button:
                result[2] = next_chap_button.get('href')
            else:
                result = None 
                print("No next chapter found.")

            return result
        else:
            print(f"The request failed with an error {response.status_code}, trying again...")
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
                    "You are a bilingual editor. Your task is to improve sloppy English translations "
                    "by comparing them with the original Chinese text. Make the English natural, fluent, "
                    "and faithful to the meaning in Chinese."
                )
            },
            {
                "role": "user",
                "content": (
                    "Original Chinese: 他昨天去了市场。\n"
                    "Machine Translated English: He go to market yesterday."
                )
            }
        ]
    )
    """

    return contentlist

# Main function
def main():
    #-------------- START ---------------
    home_url = input("What's the homepage URL (novelbin): ")
    response = requests.get(home_url)
    if response != 200:
        print(f"The request failed with an error {response.status_code}")
        sys.exit(1)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    bookFile = input("What do you want the filename to be: ")
    

    """NEED TO ADD ALL THE ERROR HANDLING"""


    book = epub.EpubBook()

    print(soup.prettify())

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
        title = title_elem.text

    book.set_title(title) 

    #-------------- Set Cover Image --------------
    img_elem = soup.find(name='img', class_='lazy')
    response = requests.get(img_elem.get('src'))
    if response.status_code == 200:
        cover_image = response.content
        print("Image Found")
        book.set_cover('cover.jpg', cover_image)
    else:
        print(f"The request failed with an error {response.status_code}")
    
    #-------------- Set Author --------------
    author_elem = soup.find(name='h3', string='Author:').find_next('a')
    book.add_author(author_elem.text)

    #-------------- Build the Chapters --------------
    toc = []
    book.spine = ['nav']

    next_chapter = soup.find(name='a', class_='btn-read-now').get('href')
    i = 1
    while not next_chapter == None:
        #-------------- Get Chapter & Next Link --------------
        contentlist = fetch_text(url,i)
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
        url = contentlist[2]


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
    epub.write_epub(bookFile, book, {})  

    print("Mission Complete");
    print("*Remember to move the file from this directory to downloads*")

# Call the main function
if __name__ == "__main__":
    main()
