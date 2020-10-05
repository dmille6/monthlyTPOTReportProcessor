import multiprocessing
from multiprocessing import Process, Manager, Pool
from memory_profiler import profile
from datetime import datetime
import orjson #opensource json parsing library, much faster
from pprint import pprint
import os, sys, json
from tqdm import tqdm

class tpotLogProcessor:
    def __init__(self, config):
        print ("tpotLogReader Object Created")

        manager = Manager()
        self.LogDirectory=config['logFolder']
        self.LogExtension=config['logFileExtension']
        self.dataDict=manager.dict()
        self.inputFilelist = []
        self.jsonList=manager.list()
        self.cpu_no=multiprocessing.cpu_count()
        self.processes = []
        self.getFileList()
        print (self.inputFilelist)

        print ("---=============================---")
        print ("Beginning to Process:")
        print("---=============================---")

    def processFiles(self, cpuCount):
        multi_lock = multiprocessing.Lock()
        multi_manager = Manager()
        shared_dict=multi_manager.dict()

        if cpuCount !=0:
            self.cpu_no = cpuCount
        else:
            self.cpu_no = multiprocessing.cpu_count()

        print ("Processing with ", self.cpu_no, " CPU cores" )
        full_startTime=datetime.now()
        for file in self.inputFilelist:
            proc = Process(target=self.multiReadFiles, args=(file,shared_dict))
            self.processes.append(proc)
            proc.start()

        # complete the processes
        for item in self.processes:
            item.join()

        print ("Total Time Taken:", datetime.now()-full_startTime)
        regDict={}
        regDict=shared_dict.copy()
        self.saveDataCSV(regDict)


    def saveDataCSV(self, data):
        fileWriter=open("output.csv", "w")
        for item in data:
            strToWrite=item + "," + str(data[item]) + "\n"
            fileWriter.write(strToWrite)
        fileWriter.close()

    def getFileList(self):
        print ("get file list")
        print(" ---: reading input files from : ", self.LogDirectory)
        for file in os.listdir(self.LogDirectory):
            if file:
                strFilename = os.path.join(self.LogDirectory, file)
                if self.LogExtension in strFilename:
                    self.inputFilelist.append(strFilename)
                    print ("   - ", strFilename)
                else:
                    print("Not Important:", strFilename)

    def multiReadFiles(self, strFileName, dataDict):
        #print ("  Processing:", strFileName)
        file_startTime = datetime.now()
        count=0
        #print("ReadFile")
        #print("Multi     - Reading ", strFileName)
        try:
            with open(strFileName, "r") as filehandler:
                for line in filehandler:
                    count+=1
                    #print (strFileName)
                    #jsonDict=json.loads(line) # python internal json parser
                    jsonDict = orjson.loads(line)  # opensource json parsing library, MUCH faster, like 60% faster than pythons json library
                    self.saveDataToDict(jsonDict, dataDict, strFileName)
            #print ("       ", strFileName, " has #", count, " lines")
            print("     Time taken to process:", strFileName, " : ", datetime.now() - file_startTime)
        except:
            e = sys.exc_info()[0]
            #print("ERROR:", e, line)
            errorString = "LoadFile ERROR: " + line + " : " + str(e) + "\n"

    def saveDataToDict(self, item, dataDict, file):
        if item['src_ip'] in dataDict:
            #print ("file:", file, " Increment:", item['src_ip'], ":", dataDict[item['src_ip']] )
            dataDict[item['src_ip']]+=1
        else:
            dataDict[item['src_ip']]=1
            #print("file:", file, " New:", item['src_ip'])


# not used **************
    def readFile(self, strFileName, dataDict):
        print ("ReadFile")
        print("     - Reading ", strFileName)
        with open(strFileName, "r") as filehandler:
            for line in filehandler:
                try:
                    if line[0] != "#":  # skip lines that are a comment
                        line = line.replace("\n", "")
                        #jsonDict=json.loads(line) # python internal json parser
                        jsonDict=orjson.loads(line) # opensource json parsing library, MUCH faster, like 60% faster
                        if "src_ip" in jsonDict:
                            if "type" in jsonDict:
                                if "P0f" in jsonDict['type'] or "Fatt" in jsonDict['type']:
                                    test=1
                                elif "Cowrie" in jsonDict['type']:
                                    test=1
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
                                    test=1
                except:
                    e = sys.exc_info()[0]
                    #print("ERROR:", e, line)
                    errorString = "LoadFile ERROR: " + line + " : " + str(e) + "\n"
