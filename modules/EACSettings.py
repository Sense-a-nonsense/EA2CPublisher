import os

## User settings 
class UserSettings(object):
    
    def __init__(self) -> None:
        self.url = str
        self.PAT = str
        self.publish_path = str
        self.req_root = str
        self.space = str
    # Read user settings from config file
    def load(self):
        settings = dict()
        with open(os.path.dirname(__file__) + '/../settings.cfg') as settings_file:
            for line in settings_file:
                setting = line.split(':', 1)
                settings[setting[0].strip(' ')] = setting[1].strip(' \n')
        self.url = settings['url']
        self.PAT = settings['PAT']
        self.space = settings['requirements_space']
        self.publish_path = str(settings['publish_path']).strip('\\')
        self.req_root = settings['requieremnts_rootpage']
    
    # Validate connection settings   
    def validate(self):
        ### TO DO ###
        pass
