

class Context:
    def __init__(self, links, text):
        self.links = links
        self.text = text
        
    def return_text(self):
        return "IMPLEMENT TEZXT IN FRONTEND"
        if (self.text != 'n/a' or self.text != 'N/A'):
            return self.text#IMPLEMENT SPLITTING INTO SEPARATE TEXTS OR LINKS
    
    def return_link(self):
        print(self.links)
        if (self.links != 'n/a' or self.link != 'N/A'):
            return self.links#IMPLEMENT
    
    def return_both(self):
        return self.return_text() + self.return_link()