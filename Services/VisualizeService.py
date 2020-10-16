import secrets
import json

from shapely.geometry import Point, shape
from shapely.geometry.polygon import Polygon


class VisualizeService():
    def __init__(self):
        return
    
    def getFormattedData(self, dataset, xAxis, yAxis):
        color = ['rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)']


        data = {}
        

        for line in dataset:
            if line[xAxis] in data:
                data[line[xAxis]] += round(float(line[yAxis]))
            else:
                data[line[xAxis]] = round(float(line[yAxis]))
        
        datacollection = {}
        datacollection['datasets'] = []
        datacollection['labels'] = []


        datasetObj = {'label':'', 
                      'data':[],
                      'backgroundColor':[],
                      'borderColor': [],
                      'borderWidth': 1,
                      'fill': False}

        for key, value in data.items():
            datacollection['labels'].append(key)
            datasetObj['data'].append(value)
            datasetObj['label'] = yAxis
            randomColor = secrets.choice(color)
            datasetObj['backgroundColor'].append(randomColor)
            datasetObj['borderColor'].append(randomColor)
        

        datacollection['datasets'].append(datasetObj)


        return datacollection


    def getMap(self, dataset, loc_col, data_col):

        checkName = True

        #the geojson file with the borders, the shape file
        with open("Services/IND_adm1.geojson", encoding="utf-8") as read_file:
            area = json.load(read_file)

        print("opened file")
        #assign the color fill to each line
        colors =[(237,248,233), (186,228,179), (116,196,118), (49,163,84), (0,109,44)] #GREEN
        #colors = [(239,243,255), (189,215,231), (107,174,214), (49,130,189), (8,81,156)] BLUE
        numColors = len(colors)
       

        if checkName:
            #get the high and low so that the right color can be assigned when giving it the data 
            low = int(dataset[0] [data_col])
            high = int(dataset[0][data_col])


            for line in dataset:
                x = int(line[data_col])
                high = max(x, high)
                low = min(x,low)

            print("Got high and low")
            print(low)
            print(high)

            bucketSize = (high - low)/numColors

            for line in area["features"]:
                name = line["properties"]["NAME_1"]
                found_match = False
                print("LINEEEEEEEEEEEEEE")
                print(line["properties"])
                for dataset_line in dataset:
                    print("looking")
                    print(dataset_line)
                    if name == dataset_line[loc_col]:
                        print("Starting found match")
                        num = int(dataset_line[data_col])
                        print("Not bad yet")
                        line["properties"]["data"] = num
                        print("Still not bad")
                        print(low)
                        print(high)
                        print(bucketSize)
                        bucketNum = int((num - low -1)//bucketSize)
                        print("Still not fucked")
                        print(bucketNum )
                        line["properties"]["color"] = colors[bucketNum]
                        print("Not fucked")
                        found_match = True
                        print("found match")
                        break
                if not found_match:
                    line["properties"]["data"] = 0
                    line["properties"]["color"] = colors[0]

            print("Went through features")
        else: #using location coordinates

            #update low and high as we run through the dataset
            low = int(0) #if you set it to something that is not 0 and then there is a feature that has not locations in it, the low would not be right
            high = int(dataset[0][data_col])

            #then loop through the dataset, I did the double loop this way because if the location from the dataset matches a feature, then you can break loop
            for dataset_line in dataset:
                loc = dataset_line[loc_col]
                num = int(dataset_line[data_col])
                #convert the location to a point
                result = [x.strip() for x in loc.split(',')]
                point = Point(float(result[1]), float(result[0])) #need to switch it for reason due to Shapely

                for feature in area["features"]:
                    polygon = shape(feature['geometry'])
                    if polygon.contains(point):
                        if "data" in feature["properties"]:
                            pre_num = feature["properties"]["data"] #what the data was already set to
                            high = max(high, (pre_num + num))
                            feature["properties"]["data"] = pre_num + num
                        else:
                            high = max(high, num)
                            feature["properties"]["data"] = num
                        break
                    
            bucketSize = (high - low)/numColors

            #assign all of the features colors 
            for line in area["features"]:
                if not "data" in line["properties"]:
                    line["properties"]["data"] = 0
                num = line["properties"]["data"]
                bucketNum = int((num - low)//bucketSize)
                line["properties"]["color"] = colors[bucketNum]
            
        bucketGrades = []
        for i in range(numColors):
            bucketGrades.append(int(low + i * bucketSize))


        return area, colors, bucketGrades