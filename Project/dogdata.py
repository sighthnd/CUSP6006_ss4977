import json
import pandas as pd
import geopandas as gp
import numpy as np
from shapely import geometry

comms = pd.read_csv("CommDists.csv")
comms = comms[comms.DistrictNumber < 20]
hoods = pd.read_csv("NTA-list.csv")
geoinds = {}
dfs = {}
jss = {}
maxNumdogs = {}
# Will try for tracts later if time
for geo in ['NTA','Community','Borough', 'Tract']:
    fname = 'data/' + geo + '.geojson'
    if geo == 'Tract':
        fh = open(fname, 'r')
        js = fh.readline()
        dct = json.loads(js)
        dfs[geo] = gp.GeoDataFrame.from_features(dct['features'])
    else:
        dfs[geo] = gp.GeoDataFrame.from_file(fname)
    maxNumdogs[geo] = dfs[geo]['numdogs'].max()

def get_nres(df):
    size = len(df.geometry.to_json())
    if size > 2000000:
        return 0.003
    elif size > 1500000:
        return 0.001
    elif size > 1000000:
        return 0.0005
    elif size > 500000:
        return 0.0001
    elif size > 100000:
        return 0.00005
    else:
        return 0
    
def selectDfByExt(indf, minx, miny, maxx, maxy):
    outdf = indf[(((indf['minx'] >= minx) & (indf['minx'] <= maxx)) |
                  ((indf['maxx'] >= minx) & (indf['maxx'] <= maxx)))]
    outdf = outdf[(((outdf['miny'] >= miny) & (outdf['miny'] <= maxy)) |
                   ((outdf['maxy'] >= miny) & (outdf['maxy'] <= maxy)))]
    return outdf

def selectBorough(bor):
    df_sel = dfs['Borough'][dfs['Borough']['boro_name'] == bor]
    return df_sel, [df_sel.minx.min(), df_sel.miny.min(),
                    df_sel.maxx.max(), df_sel.maxy.max()]

def selectHoodByName(hood):
    df_sel = dfs['NTA'][dfs['NTA']['ntaname'] == hood]
    minx = df_sel.minx.min()
    miny = df_sel.miny.min()
    maxx = df_sel.maxx.max()
    maxy = df_sel.maxy.max()
    print minx, miny, maxx, maxy
    zout = 0.2
    minx -= zout * (maxx - minx)
    maxx += zout * (maxx - minx)
    miny -= zout * (maxy - miny)
    maxy += zout * (maxy - miny)
    print minx, miny, maxx, maxy
    xsize = maxx - minx
    ysize = maxy - miny
    size = np.max([xsize, ysize])
    if xsize > ysize:
        miny -= (xsize - ysize) / 2
        maxy += (xsize - ysize) / 2
    else:
        minx -= (ysize - xsize) / 2
        maxx += (ysize - xsize) / 2
    print minx, miny, maxx, maxy
    df_sel = selectDfByExt(dfs['NTA'], minx, miny, maxx, maxy)
    print minx, miny, maxx, maxy
    #df_sel = clipDfExt('NTA', [minx, miny, maxx, maxy])
    res = get_nres(df_sel)
    if res > 0:
        df_sel.geometry = df_sel.geometry.simplify(res)
    return df_sel, [minx, miny, maxx, maxy]

def clipDfExt(aType, bbox):
    pList = [geometry.Point(bbox[int(abs(1.5 - i))],
                            bbox[int(i / 2)]) for i in range(4)]
    poly = geometry.Polygon([p.x, p.y] for p in pList)
    clipExt = gp.GeoSeries(poly)
    clipFr = dfs[aType][['geometry','id']].head(1)
    clipFr.geometry = clipExt
    return gp.overlay(dfs[aType], clipFr, how='intersection')

def selectHoodByExt(minx, miny, maxx, maxy):
    xsize = maxx - minx
    ysize = maxy - miny
    size = np.max([xsize, ysize])
    df_sel = selectDfByExt(dfs['NTA'], minx, minx, maxx, maxy)
    res = get_nres(df_sel)
    if res > 0:
        df_sel.geometry = df_sel.geometry.simplify(res)
    return df_sel

def getHoods():
    minx = dfs['NTA'].minx.min()
    miny = dfs['NTA'].miny.min()
    maxx = dfs['NTA'].maxx.max()
    maxy = dfs['NTA'].maxy.max()
    xsize = maxx - minx
    ysize = maxy - miny
    if xsize > ysize:
        miny -= (xsize - ysize) / 2
        maxy += (xsize - ysize) / 2
    else:
        minx -= (ysize - xsize) / 2
        maxx += (ysize - xsize) / 2
    ret = dfs['NTA']
    resol = get_nres(ret)
    ret.geometry = dfs['NTA'].geometry.simplify(resol)
    return ret, [minx, miny, maxx, maxy]

def selectTractsByExt(bbox):
    #df_sel = clipDfExt('Tract', bbox)
    df_sel = selectDfByExt(dfs['Tract'], bbox[0], bbox[1], bbox[2], bbox[3])
    res = get_nres(df_sel)
    if res > 0:
        df_sel.geometry = df_sel.geometry.simplify(res)
    return df_sel
