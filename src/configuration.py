import sys, os, yaml

class Configuration:
    def __init__(self, filePath:str = 'config.yaml') -> None:
        self.file = yaml.safe_load(open(filePath, 'r'))
        
