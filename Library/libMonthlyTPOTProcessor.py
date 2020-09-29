from multiprocessing import Process, Manager, Pool
from pprint import pprint
import os, sys, json

class tpotLogProcessor:

    def __init__(self, config):
        print ("tpotLogReader Object Created")

        manager = Manager()
        self.LogDirectory=config['logFolder']
        self.LogExtension=config['logFileExtension']
        #self.dataDict=manager.dict()
        self.dataDict = {}

        self.getFileList()
        print (self.inputFilelist)

        for file in self.inputFilelist:
            self.readFile(file, self.dataDict)

    def getFileList(self):
        print ("get file list")

        self.inputFilelist = []
        print(" ---: reading input files from : ", self.LogDirectory)
        for file in os.listdir(self.LogDirectory):
            if file:
                strFilename = os.path.join(self.LogDirectory, file)
                if self.LogExtension in strFilename:
                    self.inputFilelist.append(strFilename)
                    print ("   - ", strFilename)
                else:
                    print("Not Important:", strFilename)

    def readFile(self, strFileName, dataDict):
        print ("ReadFile")
        print("     - Reading ", strFileName)
        with open(strFileName, "r") as filehandler:
            for line in filehandler:
                try:
                    if line[0] != "#":  # skip lines that are a comment
                        line = line.replace("\n", "")
                        #print ("   - line:", line)
                        jsonDict=json.loads(line)
                        #print (jsonDict['src_ip'],":", jsonDict['type'], ":",jsonDict)
                        if "src_ip" in jsonDict:
                            #print (jsonDict['src_ip'])
                            if "type" in jsonDict:
                                if "P0f" in jsonDict['type'] or "Fatt" in jsonDict['type']:
                                    test=1
                                elif "Cowrie" in jsonDict['type']:
                                    if jsonDict['session']:
                                        pprint (jsonDict)
                                elif "Suricata" in jsonDict['type']:
                                    test=1
                                elif "Rdpy" in jsonDict['type']:
                                    test = 1
                                elif "Glutton" in jsonDict['type']:
                                    test = 1
                                elif "Dionaea" in jsonDict['type']:
                                    test = 1
                                elif "Heralding" in jsonDict['type']:
                                    test = 1
                                elif "Adbhoney" in jsonDict['type']:
                                    test = 1
                                elif "CitrixHoneypot" in jsonDict['type']:
                                    test = 1
                                elif "Tanner" in jsonDict['type']:
                                    test = 1
                                elif "Mailoney" in jsonDict['type']:
                                    test = 1
                                elif "ConPot" in jsonDict['type']:
                                    test = 1
                                elif "Honeypy" in jsonDict['type']:
                                    test = 1
                                elif "Ciscoasa" in jsonDict['type']:
                                    test = 1
                                elif "ssh-rsa" in jsonDict['type']:
                                    test = 1
                                else:
                                    print("    Type:", jsonDict['type'])
                                    # if jsonDict['src_ip'] in dataDict:
                                    #     tempArray = []
                                    #     tempArray.append(jsonDict)
                                    #     dataDict[jsonDict['src_ip']] = tempArray.copy()
                                    #     tempArray.clear()
                                    # else:
                                    #     dataDict[jsonDict['src_ip']]=[]
                                    #     tempArray=[]
                                    #     tempArray.append(jsonDict)
                                    #     dataDict[jsonDict['src_ip']]=tempArray.copy()
                                    #     tempArray.clear()
                except:
                    e = sys.exc_info()[0]
                    print("ERROR:", e, line)
                    errorString = "LoadFile ERROR: " + line + " : " + str(e) + "\n"
        # inputFiles[strFilename] = fileData.copy()
        # fileData.clear()
        # filehandler.close()
        # return inputFiles.copy()
