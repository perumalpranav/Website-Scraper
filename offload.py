#!/usr/bin/python3

import requests  # For sending HTTP requests and receiving HTTP responses
from bs4 import BeautifulSoup  # For parsing HTML and XML documents
from ebooklib import epub


chapterdict = {
    1: [1195427,"A New Beginning"],
    2: [1195430,"Jackpot"],
    3: [1195435,"The First Step"],
    4: [1195439,"New Horizons"],
    5: [1195444,"The Vastaire Ruins"],
    6: [1195446,"Change"],
    7: [1195447,"The Governor's Plan"],
    8: [1195458,"Greenside"],
    9: [1195469,"Rock Bottom"],
    10: [1195574,"Getting Back Up"],
    11: [1195578,"Making a Bet"],
    12: [1195582,"Virya"],
    13: [1195584,"The Correct Answer"],
    14: [1195588,"Pushing Your Limits"],
    15: [1195618,"Decisions"],
    16: [1198905,"A Choice for a Lifetime"],
    17: [1200030,"Mana Lesson"],
    18: [1201081,"Favor"],
    19: [1202198,"The First Seal"],
    20: [1203272,"Orange Grade"],
    21: [1206519,"New Possibilities"],
    22: [1207605,"Unexpected Events"],
    23: [1208639,"Journey Home"],
    24: [1209744,"Interesting Findings"],
    25: [1210748,"The Voice of the Ancestors"],
    26: [1213907,"Pushing Forward"],
    27: [1214986,"Consequences"],
    28: [1216054,"Seventh Birthday"],
    29: [1217079,"Satisfaction"],
    30: [1218092,"Legendary Specimen"],
    31: [1221319,"Time to do some Alchemy"],
    32: [1222442,"Alchemic Extravaganza"],
    33: [1224722,"The Fortuna"],
    34: [1225811,"Merfolk Merchants"],
    35: [1228863,"Big Money"],
    36: [1229949,"Taking a Gamble"],
    37: [1232010,"Marathon"],
    38: [1233022,"Fruitful Day"],
    39: [1235924,"Stupid Mushroom"],
    40: [1237013,"Unexpected"],
    41: [1238906,"Progress"],
    42: [1240093,"An Opportunity"],
    43: [1243206,"The Veeryd Jungle"],
    44: [1244516,"Brave or Reckless"],
    45: [1246810,"Hard Truths"],
    46: [1248076,"An Exemplary Teacher"],
    47: [1251168,"The Wandering Moon"],
    48: [1252258,"Silvertongue"],
    49: [1254357,"Trust"],
    50: [1255504,"Moving Forward"],
    51: [1258363,"The Ceremony"],
    52: [1259532,"The Great Spirit"],
    53: [1261601,"Maze"],
    54: [1262674,"Procession"],
    55: [1265708,"Truth"],
    56: [1266750,"Rage"],
    57: [1268915,"An Eye for an Eye"],
    58: [1269972,"The Price of Our Choices"],
    59: [1272813,"Back at the Estate"]
}

# Function to fetch text from a given URL
def fetch_text(url,i):
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')
        element = soup.find(class_='chapter-inner chapter-content')
        if element:
            print(f'Chapter {i} has been found')
            inner_html = str(element)
            return inner_html
        else:
            print(f'ALERT ALERT Chapter {i} has NOT been found')
            return '404'
    return 'Access Error'

# Function to create chapter in epub book
def create_chap(book,content,i):
    title = chapterdict.get(i)
    title = title[1]
    fname = 'chap_' + str(i) + '.xhtml'
    chapter = epub.EpubHtml(title=title, file_name=fname, lang='en')
    chapter.content = f'<h1>{title}</h1><p>{content}</p>'
    book.add_item(chapter)
    return chapter

# Main function
def main():
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier('id1')
    book.set_title('Elydes Book 1')
    book.set_language('en')

    # Add author
    book.add_author('Drewells')

    toc = []
    book.spine = ['nav']
    for i in range (1,60):
        chaplist = chapterdict.get(i)
        iden = chaplist[0]
        url = f'https://www.royalroad.com/fiction/67742/elydes/chapter/{iden}/c'
        toc.append(epub.Link(f'chap_{i}.xhtml',chaplist[1],f'chapter_{i}'))
        content = fetch_text(url,i)
        chap = create_chap(book,content,i)
        book.spine.append(chap)


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
    epub.write_epub('elydes_book1.epub', book, {})

    print("Mission Complete");


# Call the main function
if __name__ == "__main__":
    main()
