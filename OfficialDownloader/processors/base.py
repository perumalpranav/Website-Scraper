#Abstract Class for all the different websites that will be used

class WebsiteStructure:
    def __init__(self, domain_name, base_url=None):
        self.domain_name = domain_name
        self.base_url = base_url

    #Find Title
    def find_title(self, data):
        raise NotImplementedError("Subclasses must implement this method.")
    
    #Find Cover Image
    def find_cover_image(self, data):
        raise NotImplementedError("Subclasses must implement this method.")

    #Find Author Name    
    def find_author_name(self, data):
        raise NotImplementedError("Subclasses must implement this method.")

    #Find First Read (From Home Page)    
    def find_first_read(self, data):
        raise NotImplementedError("Subclasses must implement this method.")

    #Find Next Chapter (From a chapter)    
    def find_next_chapter(self, data):
        raise NotImplementedError("Subclasses must implement this method.")

    #Find Chapter Title (From a chapter)    
    def find_chapter_title(self, data):
        raise NotImplementedError("Subclasses must implement this method.")
    
    #Find Chapter Text (From a chapter)    
    def find_chapter_text(self, data):
        raise NotImplementedError("Subclasses must implement this method.")




