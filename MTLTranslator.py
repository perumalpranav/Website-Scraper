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

    while True:
        print(f'Try Chapter {i}')
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.content
            soup = BeautifulSoup(page_content, 'html.parser')

            titleelem = soup.find(class_='font-white break-word') #find chapter title element
            if titleelem:
                result[0] = titleelem.text
            else:
                result[0] = f'Chapter {i}'


            bodyelem = soup.find(class_='chapter-inner chapter-content')
            if bodyelem:
                print(f'Chapter {i} has been found')
                inner_html = str(bodyelem)
                result[1] = inner_html
            else:
                print(f'ALERT ALERT Chapter {i} has NOT been found')
                result[1] = "Not Found"

            nelems = soup.find_all(class_='btn btn-primary col-xs-12')
            for n in nelems:
                if(n.text.strip() == "Next Chapter"):
                    nextelem = n
                    break

            if nextelem:
                try:
                    result[2] = "https://www.royalroad.com" + nextelem['href']  #CHANGE THIS FOR OTHER WEBSITES
                except KeyError:
                    result[2] = "bad url"
            else:
                print("NEXT CHAPTER FAILED")

            return result

# Function to create chapter in epub book
def create_chap(book,contentlist,i):
    title = contentlist[0]
    content = contentlist[1]
    fname = 'chap_' + str(i) + '.xhtml'
    chapter = epub.EpubHtml(title=title, file_name=fname, lang='en')
    chapter.content = f'<h1>{title}</h1><p>{content}</p>'
    book.add_item(chapter)
    return chapter

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
    bookFile = input("What do you want the filename to be: ")
    response = requests.get(home_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    


    #ADD ALL THE ERROR HANDLING


    book = epub.EpubBook()

    #-------------- Set Metadata --------------
    book.set_identifier(f"urn:uuid:{uuid.uuid4()}")
    book.set_language('en')

    #-------------- Set Title --------------
    title_elem = soup.find(name='h3', class_='title')
    book.set_title(title_elem.text) 

    #-------------- Set Cover Image --------------
    img_elem = soup.find(name='img', class_='lazy')
    response = requests.get(img_elem.get('src'))
    if response.status_code == 200:
        cover_image = response.content
        print("Image Found")
        book.set_cover('cover.jpg', cover_image)
    else:
        print("Failed to download image:", img_elem.get('src'))
    
    #-------------- Set Author --------------
    author_elem = soup.find(name='h3', string='Author:').find_next('a')
    book.add_author(author_elem.text)

    #-------------- Build the Chapters --------------
    toc = []
    book.spine = ['nav']

    next_chapter = soup.find(name='a', class_='btn-read-now').get('src')
    i = 1
    while not next_chapter == None:
        ###IGNORE FOR NOW
        contentlist = fetch_text(url,i)
        #contentlist = grammar_police(contentlist)
        toc.append(epub.Link(f'chap_{i}.xhtml',contentlist[0],f'chapter_{i}'))
        chap = create_chap(book,contentlist,i)
        book.spine.append(chap)

        i += 1
        url = contentlist[2]
        ###IGNORE FOR NOW


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
