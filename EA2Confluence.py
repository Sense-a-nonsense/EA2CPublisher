import modules.EACSettings as eas
import modules.EAParser as eap
import modules.EACPublisher as eapb

### MAIN ###
### Read user settings
settings = eas.UserSettings()
settings.load()
settings.validate()

### Get documents
user_documents = eap.get_documents(settings)

### Publish documents
for document in user_documents:

    ## Prepare document for publication
    document.load_text()
    document.load_img()

    ## Search for page in confluence
    page = eapb.Page()
    page.title = document.title
    eapb.search_for_page(settings, page)

    ## Prepare page for publication
    page.version += 1
    page.body = document.body
    page.embedd_img(document)

    ## Send to confluence
    if page.version > 1:
        responce = eapb.update_page(settings, page)
    else:
        parentPage = eapb.Page()
        parentPage.title = document.parent_title
        eapb.search_for_page(settings, parentPage)
        responce = eapb.create_page(settings, page, parentPage)


    