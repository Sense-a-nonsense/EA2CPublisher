import requests
import base64
import modules.EACSettings as eas
import modules.EAParser as eap

## Confluence page
class Page(object):
    def __init__(self) -> None:
        self.body = str
        self.version = int
        self.title = str
        self.id = str
        self.parent = str
 
    # Write images into file body
    def embedd_img(self, doc: eap.EADocument):
        for image_name in doc.images:
            with open(doc.path + image_name, 'rb') as image_file:
                b64_image = str(base64.b64encode(image_file.read())).strip("b'")
            self.body = self.body.replace(image_name, 'data&colon;image/png;base64,' + b64_image)



## Search for page with specific title
def search_for_page(settings: eas.UserSettings, page: Page):
    responce = requests.get(
        url=settings.url + '/rest/api/content/',
        headers={
            'Authorization': settings.PAT
        },
        params={
            'title': page.title, 
            'spaceKey': settings.space,
            'expand': 'version,body.storage'
        }
    ).json()
    if responce['size'] == 1: 
        page.version = responce['results'][0]['version']['number']
        page.body = responce['results'][0]['body']['storage']['value']
        page.id = responce['results'][0]['id']
    elif responce['size'] == 0:
        page.version = 0

    else:
        pass
    return page

## Update page
def update_page(settings: eas.UserSettings, newPage: Page):
    request = requests.put(
        url= settings.url + '/rest/api/content/' + newPage.id,
        headers={
            "Content-Type": "application/json", 
            "Authorization": settings.PAT
        },
        json={
            "version": {
                "number": newPage.version
            },
            "title": newPage.title,
            "type": "page",
            "body": {
                "storage": {
                    "value": "<p class=\"auto-cursor-target\"><br /></p><ac:structured-macro ac:name=\"html\" ac:schema-version=\"1\" ac:macro-id=\"13583bc4-ca4e-4536-9054-801b8eb15a86\"><ac:plain-text-body><![CDATA[" + newPage.body + "]]></ac:plain-text-body></ac:structured-macro><p><br /></p>",
                    "representation": "storage"
                }
            }
        }
    )
    return request

## Create new page
def create_page(settings: eas.UserSettings, newPage: Page, parentPage: Page):

    request = requests.post(
        url= settings.url + '/rest/api/content/',
        headers={
            "Content-Type": "application/json", 
            "Authorization": settings.PAT
        },
        json={
            "title": newPage.title,
            "space": {
                "key": settings.space
            },
            "status": "current",
            "ancestors": [
                {
                    "id": parentPage.id
                }
            ],
            "type": "page",
            "body": {
                "storage": {
                    "value": "<p class=\"auto-cursor-target\"><br /></p><ac:structured-macro ac:name=\"html\" ac:schema-version=\"1\" ac:macro-id=\"13583bc4-ca4e-4536-9054-801b8eb15a86\"><ac:plain-text-body><![CDATA[" + newPage.body + "]]></ac:plain-text-body></ac:structured-macro><p><br /></p>",
                    "representation": "storage"
                }
            }
        }
    )
    return request