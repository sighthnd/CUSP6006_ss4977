import json
from flask import Flask, Response
import pandas as pd
import dogdata as dog

app = Flask(__name__, static_url_path='', static_folder='.')
app.add_url_rule('/', 'root', lambda: app.send_static_file('dogs.html'))
resp_heads = {'Cache-Control': 'no-cache',
              'Access-Control-Allow-Origin': '*'}

@app.route('/makemap/<geotype>/<borough>/<subarea>/<tracts>')
def serve(geotype, borough, subarea, tracts):
    answering = 0
    borough = borough.replace('%20', ' ')
    subarea = subarea.replace('%20', ' ')
    if geotype == 'borough':
        pass
    elif geotype == 'comms':
        if borough == 'full': # Full city
            pass
        else:
            if subarea == 'full': # Full borough
                pass
            else:
                if tracts == 'yes':
                    pass
                else:
                    pass
    elif geotype == 'nta':
        if borough == 'full': # Full city
            answering = 1
            territory, bbox = dog.getHoods()
            response = "[{}, {}]".format(json.dumps(bbox),
                                         territory.to_json())
        else:
            if subarea == 'full': # Full borough
                answering = 1
                territory, bbox = dog.selectBorough(borough)
                territory = dog.selectHoodByExt(bbox[0], bbox[1],
                                                bbox[2], bbox[3])
                #territory = dog.clipDfExt('NTA', bbox)
                response = "[{},{}]".format(json.dumps(bbox),
                                            territory.to_json())
            else:
                territory, bbox = dog.selectHoodByName(subarea)
                territory = dog.selectHoodByExt(bbox[0], bbox[1],
                                                bbox[2], bbox[3])
                if tracts == 'Yes':
                    answering = 1
                    tracts = dog.selectTractsByExt(bbox)
                    response = "[{},{},{}]".format(json.dumps(bbox),
                                                   tracts.to_json(),
                                                   territory.to_json())
                else:
                    answering = 1
                    response = "[{},{}]".format(json.dumps(bbox),
                                                territory.to_json())
    if answering == 1:
        # Debugging responses
        #fh = open('resplog.txt', 'w')
        #fh.write(response)
        return Response(response, mimetype='application/json',
                        headers=resp_heads)
    else:
        return Response("{}", mimetype='application/json',
                        headers=resp_heads)


@app.route('/listcomms/<borough>')
def comms(borough):
    df = dog.comms
    df = df[(df.Borough == borough) & (df.DistrictNumber < 20)]
    response = json.dumps(sorted(df.DistrictNumber.tolist()))
    return Response(response,
                    mimetype='application/json',
                    headers=resp_heads)
    
@app.route('/listhoods/<borough>')
def hoods(borough):
    df = dog.hoods
    df = df[(df.boro_name == borough) & (df.ntaname.str[:4] != 'park')]
    arr = sorted(df.ntaname.tolist())
    response = json.dumps(sorted(arr))
    return Response(response,
                    mimetype='application/json',
                    headers=resp_heads)


if __name__ == '__main__':
    app.run(port=8002)
