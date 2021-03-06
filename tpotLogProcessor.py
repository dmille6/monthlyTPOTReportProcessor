import yaml
from Library import libMonthlyTPOTProcessor
from datetime import datetime
from memory_profiler import profile

if __name__ == "__main__":
    print ("tpotLogProcessor")

    with open(r'./tpotReader.yaml') as file:
        tpotLogReader_config = yaml.load(file, Loader=yaml.FullLoader)
        print (tpotLogReader_config)

    tpotReaderObj = libMonthlyTPOTProcessor.tpotLogProcessor(tpotLogReader_config)

    start_time=datetime.now()
    tpotReaderObj.processFiles(0) #All Available Cores
    print ("CPU Cores: 16 ", "End Time:", datetime.now()-start_time)




