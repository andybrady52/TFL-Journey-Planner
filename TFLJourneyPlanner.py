print(r"""\
            ********** ******** **      
            /////**/// /**///// /**      
                /**    /**      /**      
                /**    /******* /**      
                /**    /**////  /**      
                /**    /**      /**      
                /**    /**      /********
                //     //       //////// 

    ___________   _______________________________________^__
 ___   ___ |||  ___   ___   ___    ___ ___  |   __  ,----\
|   | |   |||| |   | |   | |   |  |   |   | |  |  | |_____\
|___| |___|||| |___| |___| |___|  | O | O | |  |  |        \
           |||                    |___|___| |  |__|         )
___________|||______________________________|______________/
           |||                                        /--------
-----------'''---------------------------------------'

Welcome to TFL Journey Planner. Lets Plan Your Journey...
""")
#TFL Journey Planner
import requests
appKey = "260aa9b86dc64ce6a3f29eff869a7c66"
i = 0
ii = 0

origin = input("Enter Origin:\n")
destination = input("Enter Destination:\n")
#origin = "gallions reach"
#destination = "high barnet station"
print()

disamUrl = "https://api.tfl.gov.uk/journey/journeyresults/{0}/to/{1}?app_key={2}".format(origin, destination, appKey)
print("Url for disambiguation call")
print(disamUrl)
print()

journeyResponse = requests.get(disamUrl).json()
toLocationDisambiguation = journeyResponse['toLocationDisambiguation']['disambiguationOptions']
fromLocationDisambiguation = journeyResponse['fromLocationDisambiguation']['disambiguationOptions']


print("Possible matches for origin location:")
for fromLocation in fromLocationDisambiguation:

    print(fromLocationDisambiguation[i]['place']['commonName'])
    i += 1

print()
print()
#reset counter
i = 0
print("Possible matches for destination location:")
for toLocation in toLocationDisambiguation:

    print(toLocationDisambiguation[i]['place']['commonName'])
    i += 1

#Set origin and destination from the top disambuguation result
fromLocationIcsCode = journeyResponse['fromLocationDisambiguation']['disambiguationOptions'][0]['place']['icsCode']
toLocationIcsCode = journeyResponse['toLocationDisambiguation']['disambiguationOptions'][0]['place']['icsCode']
print()
print()
print("origin ics code: ",fromLocationIcsCode)
print("Destination location ics code: ",toLocationIcsCode)
print()
print()

print("URL for journey details")
icsCodeUrl = "https://api.tfl.gov.uk/journey/journeyresults/{0}/to/{1}?app_key={2}".format(fromLocationIcsCode, toLocationIcsCode, appKey)
icsResponse = requests.get(icsCodeUrl).json()
print(icsCodeUrl)
#noOfJourneys = len(icsResponse['journeys'])
journeys = icsResponse['journeys']

#print("data type ", type(journeys))
journeySummarys = icsResponse['journeys']
#reset counter
i = 0

for journey in journeys:
    # print("legs [0] index", journeys[i]['legs'][i]['path']['stopPoints'])
    # print("length of legs list ", len(journeys[i]['legs']))
    # print("i = ", i)
    # print("legs list index 0", journeys[i]['legs'][i])
    print("Journey", i +1)
    print("Start time:",journeys[i]['startDateTime'][-8:])
    print("arrival time:",journeys[i]['arrivalDateTime'][-8:])
    if "fare" in journeys[i]:
        fare = journeys[i]['fare']['totalCost'] / 100
        print("Fare: £%.2f" % fare)
    print("legs:")
    for summary in journeys[i]['legs']:
        print(journeys[i]['legs'][ii]['instruction']['summary'])
        ii += 1
    #reset counter
    ii = 0
    print()
    print()
    print()

    i += 1


print()
print()

#write journeys to file
file = open("journeys.txt", "w")
file.write(str(journeys))
file.close()