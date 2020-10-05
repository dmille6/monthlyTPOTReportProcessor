import yaml
from Library import libMonthlyTPOTProcessor
from memory_profiler import profile

if __name__ == "__main__":
    print ("tpotLogProcessor")

    with open(r'./tpotReader.yaml') as file:
        tpotLogReader_config = yaml.load(file, Loader=yaml.FullLoader)
        print (tpotLogReader_config)

    tpotReaderObj = libMonthlyTPOTProcessor.tpotLogProcessor(tpotLogReader_config)
    tpotReaderObj.processFiles(0) #All Available Cores
    tpotReaderObj.processFiles(8)
    tpotReaderObj.processFiles(4)
    tpotReaderObj.processFiles(2)
    tpotReaderObj.processFiles(1)



