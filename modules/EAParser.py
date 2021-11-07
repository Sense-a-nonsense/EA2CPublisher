import os
import modules.EACSettings as eas

## Published document
class EADocument(object):
    def __init__(self, path: str, id: str, title: str) -> None:
        self.id = 'EAID_' + id
        self.name = 'EAID_'+ id + '.htm'
        self.title = title
        self.parent_title = str
        self.body = str
        self.images = []
        self.path = path + '\\linkdocs\\'

    # Read published EA document   
    def load_text(self):
        with open(self.path + self.name) as data:
            for line in data:
                if str(line) == '</body>\n': break 
                self.body = str(self.body) + line.strip()
                if line == '<body>\n': self.body = '' 
    
    # Read images from this file
    def load_img(self):
        for image in os.listdir(self.path):
            if image.endswith('.PNG') and image.startswith(self.id):
                self.images.append(image)



## Parse for published documents
def get_documents (settings: eas.UserSettings):
    documents = []

    #Parse file for root id and name
    with open(settings.publish_path + '\\js\\data\\' + 'root.xml') as file:
        for line in file:
            splitline = line.lstrip('tocTab[tocTab.length] = new Array(').rstrip(');').split(', ')
            root_id = splitline[7].strip('"\{\}')
            root_name = splitline[2].strip('"')
            #if root_name != settings.req_root:
                #return documents

    #Parse root file for couments id's,  names, parents
    toc_ids =  {'0': settings.req_root}
    with open(settings.publish_path + '\\js\\data\\' + root_id + '.xml') as file:
        for line in file:
            splitline = line.lstrip('tocTab[tocTab.length] = new Array(').rstrip(');').split(',')
            if splitline[8] == ' "Artifact0"':
 
                doc_id = splitline[9].lstrip(' "{').rstrip('}");\n').replace('-', '_')
                doc_title = splitline[2].lstrip(' "В«DocumentВ» ').rstrip('"')
                self_toc_id = splitline[5].lstrip(' "{').rstrip('"')
                parent_toc_id = splitline[6].lstrip(' "{').rstrip('"')
                toc_ids[self_toc_id] = doc_title

                document = EADocument(settings.publish_path, doc_id, doc_title)
                document.parent_title = parent_toc_id
                documents.append(document)
 
    #Replace toc id's in parents for documents names
    for doc in documents: 
        doc.parent_title = toc_ids[doc.parent_title]
    return documents