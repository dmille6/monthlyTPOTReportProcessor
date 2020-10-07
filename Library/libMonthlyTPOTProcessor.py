import multiprocessing
from multiprocessing import Process, Manager, Pool
from datetime import datetime
import orjson #opensource json parsing library, much faster
import os, sys, json
from pymongo import MongoClient
import pymongo
from tqdm import tqdm


class tpotLogProcessor:
    def __init__(self, config):
        print ("tpotLogReader Object Created")

        manager = Manager()
        self.LogDirectory=config['logFolder']
        self.LogExtension=config['logFileExtension']
        self.MongoServer=config['mongoServer']
        self.dataDict=manager.dict()
        self.allDataList=manager.list()
        self.inputFilelist = []
        self.jsonList=manager.list()
        self.cpu_no=multiprocessing.cpu_count()
        self.processes = []
        self.getFileList()

        print ("---=============================---")
        print ("Beginning to Process:")
        print("---=============================---")

    def processFiles(self, cpuCount):
        multi_manager = Manager()
        shared_dict=multi_manager.dict()
        if cpuCount !=0:
            self.cpu_no = cpuCount
        else:
            self.cpu_no = multiprocessing.cpu_count()

        print ("Processing with ", self.cpu_no, " CPU cores" )
        full_startTime=datetime.now()
        for file in self.inputFilelist:
            proc = Process(target=self.multiReadFiles, args=(file,shared_dict,))
            self.processes.append(proc)
            proc.start()

        # complete the processes
        for item in self.processes:
            item.join()

        print ("Total Time Taken:", datetime.now()-full_startTime)

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
        fileDict={}
        count=0
        file_startTime = datetime.now()
        strID=strFileName
        strID=strID.replace("./Logs/","")

        print("Processing:", strFileName)
        with open(strFileName, "r") as filehandler:
            for line in filehandler:
                # jsonDict=json.loads(line) # python internal json parser
                jsonDict = orjson.loads(line)  # opensource json parsing library, MUCH faster, like 60% faster than pythons json library
                logType=jsonDict['type']
                if logType in fileDict.keys():
                    fileDict[logType].append(jsonDict)
                else: # new kind of logtype
                    fileDict[logType]=[]
                    fileDict[logType].append(jsonDict)

        #print ("File:", strFileName, "has these log types:", fileDict.keys())
        for logCat in fileDict:
            #print ("    Log Type:", logCat, " : ", len(fileDict[logCat]))
            if logCat != "Suricata":
                self.mongoInsert(fileDict[logCat], logCat)
        print ("Processing Complete for:", strFileName)

    def mongoInsert(self, dataBlock, logType):
        currentDate = datetime.now()
        monthName= currentDate.strftime('%B')
        year=currentDate.year
        strCatalogName="TPOT20-"+ logType + "-"+monthName+str(year)

        #print (strCatalogName)

        client = MongoClient(self.MongoServer)
        db = client['tpot20']
        collection_name=strCatalogName
        HP_collection = db[collection_name]
        # print ("   DataBlock Contains:", len(dataBlock))
        result=HP_collection.insert_many(dataBlock, ordered=False,bypass_document_validation=True)

