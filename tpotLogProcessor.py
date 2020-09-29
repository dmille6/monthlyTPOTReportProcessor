import yaml
from Library import libMonthlyTPOTProcessor

if __name__ == "__main__":
    print ("tpotLogProcessor")

    with open(r'./tpotReader.yaml') as file:
        tpotLogReader_config = yaml.load(file, Loader=yaml.FullLoader)
        print (tpotLogReader_config)


    tpotReaderObj = libMonthlyTPOTProcessor.tpotLogProcessor(tpotLogReader_config)


