import urllib
import json
import altair as alt

def loadData():
    # Load the data about cuisines from the remote server
    #site = "https://raw.githubusercontent.com/hvo/datasets/master/"
    #cuis_url = site + "nyc_restaurants_by_cuisine.json"
    cuis_file = "nyc_restaurants_by_cuisine.json"
    fh = open(cuis_file, 'r')
    js = fh.readline()
    # Data comes in the form of an array where each element is of the form
    # {"cuisine": <cuisine name>, "perZip": {<zip0>:<count0>, <zip1>:<count1>, ...}}
    cuis_struct = json.loads(js)

    # Need to convert that to dictionary by zip code
    # with each element containing an array of
    # {"cuisine":<cuisine_name>, "count",<number>}
    # sorted in reverse order by "count"
    zip_struct = {}
    for cuis in cuis_struct:
        cname = cuis["cuisine"]
        for zp in cuis["perZip"].keys():
            num_rests = cuis["perZip"][zp]
            # Manually perform a heap sort
            if zp in zip_struct.keys():
                lo = 0
                hi = len(zip_struct[zp]) - 1
                mid = hi / 2
                if num_rests < zip_struct[zp][hi]["count"]:
                    zip_struct[zp].append({"cuisine": cname, "count": num_rests})
                elif num_rests > zip_struct[zp][lo]["count"]:
                    zip_struct[zp].insert(0, {"cuisine": cname, "count": num_rests})
                else:
                    while hi > lo + 1:
                        if num_rests < zip_struct[zp][mid]["count"]:
                            lo = mid
                            mid = (hi + lo) / 2
                        elif num_rests > zip_struct[zp][mid]["count"]:
                            hi = mid
                            mid = (hi + lo) / 2
                        else:
                            lo = mid
                            hi = lo
                            mid = hi
                            zip_struct[zp].insert(hi, {"cuisine": cname, "count": num_rests})
            else:
                zip_struct[zp] = [{"cuisine": cname, "count": num_rests}]
    return zip_struct

def createChart(data):
    maxCount = int(data[0]["count"])
    barCount = alt.Chart(data) \
               .mark_bar(stroke="Black") \
               .encode(
                   alt.X("count:Q", axis=alt.Axis(title="Number of Restaurants")),
                   alt.Y("cuisine:O", axis=alt.Axis(title="cuisine")),
                   alt.ColorValue("LightGrey"),
               )
    return barCount
