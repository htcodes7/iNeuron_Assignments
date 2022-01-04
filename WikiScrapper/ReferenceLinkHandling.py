
class ReferenceHandler:

    def __init__(self):
        self.reference_list = []
        self.allLinks = []

    def store_links(self, soup):
        self.allLinks = soup.find(class_="references").find_all("a")
        for link in self.allLinks:
            try:
                if 'external' in link['class']:
                    self.reference_list.append(link['href'])
            except KeyError:
                continue

    def get_references(self):
        return self.reference_list
