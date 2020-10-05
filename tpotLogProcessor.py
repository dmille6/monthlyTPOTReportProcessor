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

    start_time = datetime.now()
    tpotReaderObj.processFiles(8)  # All Available Cores
    print("CPU Cores: 8 ", "End Time:", datetime.now() - start_time)

    start_time = datetime.now()
    tpotReaderObj.processFiles(4)  # All Available Cores
    print("CPU Cores: 4 ", "End Time:", datetime.now() - start_time)

    start_time = datetime.now()
    tpotReaderObj.processFiles(2)  # All Available Cores
    print("CPU Cores: 2 ", "End Time:", datetime.now() - start_time)

    start_time = datetime.now()
    tpotReaderObj.processFiles(1)  # All Available Cores
    print("CPU Cores: 1 ", "End Time:", datetime.now() - start_time)




