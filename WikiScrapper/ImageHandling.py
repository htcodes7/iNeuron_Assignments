import requests
import base64


class ImageHandler:

    def __init__(self):
        self.image_content_list = []
        self.allImages = ''
        self.decoded_images_list = []

    def encode_images(self, soup):
        self.allImages = soup.findAll('img')
        for image in self.allImages[:-2]:
            url = 'https:' + image['src']
            image_content = requests.get(url).content
            image_str = base64.b64encode(image_content)
            self.image_content_list.append(image_str)

    def get_images(self):
        return self.image_content_list

    def get_decoded_images(self, images):
        # self.decoded_images_list = []
        for img in images:
            try:
                dec_img = img.decode()
                dec_img_src = "data:image/jpeg;base64," + dec_img
                self.decoded_images_list.append(dec_img_src)
            except Exception as e:
                raise Exception("(get_decoded_images): Something went wrong while decoding stored images\n" + str(e))
        return self.decoded_images_list
