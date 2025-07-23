from .base import WebsiteStructure


#Subclass for royalroad.com
class RoyalRoad(WebsiteStructure):
    def __init__(self, domain_name, base_url=None):
        self.domain_name = domain_name
        self.base_url = base_url

    #Find Title
    def find_title(self, soup):
        title_elem = soup.find(name='div', class_='fic-title').find('h1')
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
        img_elem = soup.find(name='div', class_='cover-art-container').find(class_='thumbnail inline-block')
        return img_elem.get('src') if img_elem else None
    
    #Find Author Name    
    def find_author_name(self, soup):
        author_elem = soup.find(name='div', class_='fic-title').find('a')
        return author_elem.text if author_elem else None
    
    #Find First Read (From Home Page)    
    def find_first_read(self, soup):
        first_chapter_elem = soup.find(name='div', class_='fic-buttons').find('a')
        if first_chapter_elem is not None:
            end = first_chapter_elem.get('href')
            if end is not None:
                    return f"https://www.royalroad.com{end}"
        
        return None

    #Find Next Chapter (From a chapter)    
    def find_next_chapter(self, soup):
        next_chap_buttons = soup.find_all(class_='btn btn-primary col-xs-12')
        for n in next_chap_buttons:
            if(n.text.strip() == "Next Chapter"):
                nextelem = n
                break

        if nextelem:
            end = nextelem.get('href')
            if end is not None:
                return f"https://www.royalroad.com{end}" 
            
        return None
