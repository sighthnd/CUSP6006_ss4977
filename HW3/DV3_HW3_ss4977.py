import urllib
import altair as alt
import json
from flask import Flask, Response
from HW3_analysis import loadData, createChart

data = loadData()

app = Flask(__name__, static_url_path='', static_folder='.')
app.add_url_rule('/', 'root', lambda: app.send_static_file('tmp.html'))

@app.route('/vis/<zipcode>')
def visualize(zipcode):
#    return zipcode
#
    if zipcode in data.keys():
        response = createChart(data[zipcode]).to_json()
        #response = ''
        #for cs in data[zipcode]:
        #    response += "cuisine: {:s}, number: {:d}<br>".format(cs["cuisine"], cs["count"])
    else:
        response = ''
    print response
    return Response(response,
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )

if __name__ == '__main__':
    app.run(port=8002)
