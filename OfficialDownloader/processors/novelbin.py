from .base import WebsiteStructure


#Subclass for novelbin.com
class NovelBin(WebsiteStructure):
    def __init__(self, domain_name, base_url=None):
        self.domain_name = domain_name
        self.base_url = base_url

    #Find Title
    def find_title(self, soup):
        title_elem = soup.find(name='h3', class_='title')
        if title_elem is None:
            ans = input("TITLE NOT FOUND, would you like to manually enter it (Y/N): ")
            if ans == 'y' or ans == 'Y':
                book_title = input("Enter Book Title: ")
            else:
                print("Quitting...")
                return None
        else:
            book_title = title_elem.text

        return book_title
    
    #Find Cover Image
    def find_cover_image(self, soup):
        img_elem = soup.find(name='img', class_='lazy')
        return img_elem.get('data-src') if img_elem else None
    
    #Find Author Name    
    def find_author_name(self, soup):
        author_elem = soup.find(name='h3', string='Author:').find_next('a')
        return author_elem.text if author_elem else None
    
    #Find First Read (From Home Page)    
    def find_first_read(self, soup):
        first_chapter_elem = soup.find(name='a', class_='btn-read-now')
        return first_chapter_elem.get('href') if first_chapter_elem else None

    #Find Next Chapter (From a chapter)    
    def find_next_chapter(self, soup):
        next_chap_button = soup.find(name='a', id='next_chap', class_=['btn', 'btn-success'])
        if next_chap_button and not next_chap_button.has_attr("disabled"):        
            return next_chap_button.get('href')
        else:
            return None
        
    #Find Chapter Title (From a chapter)    
    def find_chapter_title(self, soup, i):
        titleelem = soup.find(name='a', class_='chr-title')
        return titleelem.get('title') if titleelem else f'Chapter {i}'
    
    #Find Chapter Text (From a chapter)    
    def find_chapter_text(self, soup):
        bodyelem = soup.find(name='div', class_='chr-c', id='chr-content')
        return str(bodyelem) if bodyelem else None