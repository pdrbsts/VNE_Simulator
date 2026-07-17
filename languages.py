# Source Generated with Decompyle++
# File: extract/AC_SIM.exe_extracted/PYZ-00.pyz_extracted/languages.pyc (Python 3.9)

from threading import *

class Languages:
    '''
    Thread safe, le funzioni in scrittura fanno lock/unlock
    '''
    __instance = None
    
    class __Languages:
        """
        Puo' lanciare l'eccezione IOError, se il file indicato alla creazione non esiste
        """
        lock = None
        fileName = None
        propertyDict = None
        
        def __init__(self, fileNameArg):
            self.lock = Lock()
            self.fileName = fileNameArg
            self.propertyDict = dict()
            with open(fileNameArg, 'r') as propFile:
                for propLine in propFile:
                    propDef = propLine.strip()
                    if len(propDef) == 0:
                        continue
                    if propDef[0] in ('!', '#'):
                        continue
                    punctuation = [propDef.find(c) for c in ':= '] + [len(propDef)]
                    found = min([pos for pos in punctuation if pos != -1])
                    name = propDef[:found].rstrip()
                    value = propDef[found:].lstrip(':= ').rstrip()
                    self.propertyDict[name] = value.replace('\\n', '\n')

        
        def get(self, propKey):
            if self.propertyDict != None:
                return self.propertyDict.get(propKey)
            return None

        
        def change(self, fileNameArg):
            self.lock = Lock()
            self.fileName = fileNameArg
            self.propertyDict = dict()
            with open(fileNameArg, 'r') as propFile:
                for propLine in propFile:
                    propDef = propLine.strip()
                    if len(propDef) == 0:
                        continue
                    if propDef[0] in ('!', '#'):
                        continue
                    punctuation = [propDef.find(c) for c in ':= '] + [len(propDef)]
                    found = min([pos for pos in punctuation if pos != -1])
                    name = propDef[:found].rstrip()
                    value = propDef[found:].lstrip(':= ').rstrip()
                    self.propertyDict[name] = value.replace('\\n', '\n')
            return 1


    
    def __init__(self, fileName):
        if self.__instance is None:
            Languages.__instance = Languages.__Languages(fileName)
        self.__dict__['_Languages__instance'] = Languages.__instance

    
    def getDict(self):
        return self.__instance.propertyDict

    
    def get(self, propKey):
        return self.__instance.get(propKey)

    
    def change(self, filelang):
        return self.__instance.change(filelang)


