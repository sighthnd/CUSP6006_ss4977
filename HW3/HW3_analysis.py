import urllib
import pandas as pd
import json
import altair as alt

def loadData():
    # Load the data about cuisines from the remote server
    #site = "https://raw.githubusercontent.com/hvo/datasets/master/"
    cuis_file = "nyc_restaurants_by_cuisine.json"
    #cuis_url = site + cuis_file
    fh = open(cuis_file, 'r')
    js = fh.readline()
    # Data comes in the form of an array where each element is of the form
    # {"cuisine": <cuisine name>, "perZip": {<zip0>:<count0>, <zip1>:<count1>, ...}}
    cuis_struct = json.loads(js)

    # Need to convert that to dictionary by zip code
    # with each element containing an array of
    # {"cuisine":<cuisine_name>, "count",<number>}
    zip_struct = {}
    for cuis in cuis_struct:
        cname = cuis["cuisine"]
        for zp in cuis["perZip"].keys():
            num_rests = cuis["perZip"][zp]
            # Manually perform a heap sort
            if zp in zip_struct.keys():
                zip_struct[zp].append({"cuisine": cname, "count": num_rests})
            else:
                zip_struct[zp] = [{"cuisine": cname, "count": num_rests}]
    return zip_struct

def createChart(data):
    maxCount = int(data[0]["count"])
    barCount = alt.Chart(pd.DataFrame.from_records(data)) \
               .mark_bar(stroke="Black") \
               .encode(
                   alt.X("count:Q",
                         axis=alt.Axis(title="Number of Restaurants")),
                   alt.Y("cuisine:O", axis=alt.Axis(title="cuisine"),
                         sort=alt.SortField(field="count", order="descending",
                                            op="mean")),
                   alt.ColorValue("LightGrey")
               )
    return barCount
