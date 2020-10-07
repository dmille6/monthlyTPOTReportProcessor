if jsonDict['type'] == "P0f":
    parsedJSON = self.parseP0f(jsonDict)
    if "P0f" in fileDict.keys():
        fileDict['P0f'].append(parsedJSON)
    else:
        fileDict['P0f'] = []
        fileDict['P0f'].append(parsedJSON)
elif jsonDict['type'] == "Cowrie":
    if "Cowrie" in fileDict.keys():
        fileDict['Cowrie'].append(jsonDict)
    else:
        fileDict['Cowrie'] = []
        fileDict['Cowrie'].append(jsonDict)
# elif jsonDict['type'] == "Suricata":
#     if "Suricata" in fileDict.keys():
#         jsonDict.pop('smtp', None)
#         fileDict['Suricata'].append(jsonDict)
#     else:
#         jsonDict.pop('smtp', None)
#         fileDict['Suricata'] = []
#         fileDict['Suricata'].append(jsonDict)
except:
print(jsonDict)
#         elif jsonDict['type'] == "Rdpy":
#             if "Rdpy" in fileDict.keys():
#                 fileDict['Rdpy'].append(jsonDict)
#             else:
#                 fileDict['Rdpy'] = []
#                 fileDict['Rdpy'].append(jsonDict)
#             test = 1
#         elif jsonDict['type'] == "Cowrie":
#             test = 1
#         elif jsonDict['type'] == "NGINX":
#             test = 1
#         elif jsonDict['type'] == "Mailoney":
#             test = 1
#         elif jsonDict['type'] == "Ciscoasa":
#             test = 1
#         elif jsonDict['type'] == "Honeytrap":
#             test = 1
#         elif jsonDict['type'] == "ElasticPot":
#             test = 1
#         elif jsonDict['type'] == "Dionaea":
#             test = 1
#         elif jsonDict['type'] == "Tanner":
#             test = 1
#         elif jsonDict['type'] == "ssh-rsa":
#             test = 1
#         elif jsonDict['type'] == "ConPot":
#             test = 1
#         elif jsonDict['type'] == "Adbhoney":
#             test=1
#         elif jsonDict['type'] == "Heralding":
#             test=1
#         else:
#             print (jsonDict['type'])
finally:
print("Writing Dictionary Entries.. please wait")
for hpType in fileDict:
    print("Writing: ", hpType, " ...")
    self.mongoInsert(fileDict[hpType])


    def parseP0f(self, data):
        parsedDict=data
        parsedDict.pop('path', None)
        parsedDict.pop('link', None)
        parsedDict.pop('mod', None)
        parsedDict.pop('raw_mtu', None)
        return parsedDict



