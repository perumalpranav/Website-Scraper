#!/usr/bin/python3

"""
Translates MTL novels to readable English, and saves final product as epub
"""

import requests  # For sending HTTP requests and receiving HTTP responses
from bs4 import BeautifulSoup  # For parsing HTML and XML documents
from ebooklib import epub
import ollama

#CHANGE THIS ID FOR OTHER BOOKS
idstring = input("What's the idstring: ")
# CHANGE THIS TITLE FOR OTHER BOOKS
booktitle = input("What's the title: ")
#CHANGE THIS URL FOR OTHER BOOKS
cover_url = input("Give me the cover URL: ")
#CHANGE NUMBER OF CHAPTERS
numChaps = int(input("How may chapters are we downloading(+1): "))
#START CHAPTER URL
starturl = input("What's the url for the first chapter: ")
#CHANGE THIS FILENAME FOR OTHER BOOKS
bookFile = input("What do you want the filename to be: ")


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
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier(idstring)
    book.set_title(booktitle) 
    book.set_language('en')

    response = requests.get(cover_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    img_elem = soup.find(class_='thumbnail inline-block')

    # Extract the URL of the image
    if img_elem and 'src' in img_elem.attrs:
        img_url = img_elem['src']
        img_response = requests.get(img_url)
        if img_response.status_code == 200:
            cover_image = img_response.content
            print("Image Found")
        else:
            print("Failed to download image:", img_url)
    else:
        print("No image found on the webpage.")


    book.set_cover('cover.jpg', cover_image)

    # Add author
    book.add_author('Perumal')

    toc = []
    book.spine = ['nav']
    for i in range (1,numChaps):          
        if i == 1:
            url = starturl
 
        contentlist = fetch_text(url,i)

        #contentlist = grammar_police(contentlist)


        toc.append(epub.Link(f'chap_{i}.xhtml',contentlist[0],f'chapter_{i}'))
        chap = create_chap(book,contentlist,i)
        book.spine.append(chap)
        url = contentlist[2]


    # Define Table of Contents
    book.toc = tuple(toc)

    # Add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define CSS style
    style = 'body { font-family: Times, Times New Roman, serif; }'
    nav_css = epub.EpubItem(uid='style_nav', file_name='style/nav.css', media_type='text/css', content=style)

    # Add CSS file
    book.add_item(nav_css)

    # Write to the file
    epub.write_epub(bookFile, book, {})  

    print("Mission Complete");
    print("*Remember to move the file from this directory to downloads*")

# Call the main function
if __name__ == "__main__":
    main()
