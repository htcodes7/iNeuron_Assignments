
class TextHandler:

    def __init__(self, soup):
        self.text = ''
        self.paragraphs = soup.findAll('p')
        for para in self.paragraphs[0:5]:
            self.text += para.text

    def get_summary(self):
        return self.text
