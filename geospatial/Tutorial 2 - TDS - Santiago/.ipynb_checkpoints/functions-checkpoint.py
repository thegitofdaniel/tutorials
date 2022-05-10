# general
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# geospatial
import shapefile as shp
import openpyxl

figsize = (8,8)

def read_shapefile(sf):
    # pandas & pyshp
    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df

def plot_shape(sf
               , c_id
               , s=None
               , figsize = figsize
              ):
    """ PLOTS A SINGLE SHAPE """
    plt.figure(figsize = figsize)
    ax = plt.axes()
    ax.set_aspect('equal')
    shape_ex = sf.shape(c_id)
    x_lon = np.zeros((len(shape_ex.points),1))
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]

    plt.plot(x_lon,y_lat) 
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.title("{} {}".format(s,(x0,y0)))
    # use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    plt.show()

def plot_map(sf,
             c_id=-1,
             x_lim = None,
             y_lim = None,
             figsize = figsize,
             highlight = False
            ):
    
    """
    Plot map within limiting coordinates
    """
    plt.figure(figsize = figsize)
    # add shapes to graph
    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            x = [i[0] for i in shape.shape.points[i_start:i_end]]
            y = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(x, y, 'k')
        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            plt.text(x0, y0, c_id, fontsize=10)
        c_id = c_id+1
    
    # limits
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)
    
    
    if highlight:
        shape_ex = sf.shape(c_id)
        x_lon = np.zeros((len(shape_ex.points),1))
        y_lat = np.zeros((len(shape_ex.points),1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        plt.plot(x_lon,y_lat, 'r', linewidth=3) 
    
    plt.show()
    
    
def plot_map_v2(sf,
                comuna=-1,
                title='',
                x_lim = None,
                y_lim = None,
                figsize = figsize,
                fill_comuna = -1,
                fill_color = 'g',
                annotate=True,
                border_color = 'darkgreen',
                save=False):
    
    """
    Plot map within limiting coordinates, border highlight and fill
    """
    
    # converts strings to code
    df = read_shapefile(sf)
    if isinstance(comuna[0], str):
        comuna_id = []
        for i in comuna:
            comuna_id.append(df[df.NOM_COMUNA == i.upper()]
                             .index.to_list()[0])
        comuna = comuna_id
    
    # create figure
    fig, ax = plt.subplots(figsize = figsize)
    fig.suptitle(title, fontsize=16,fontweight='bold')

    # plot shapes
    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            x = [i[0] for i in shape.shape.points[i_start:i_end]]
            y = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(x, y, 'k')
    
    # fill in comunas            
    if comuna != -1:
        for c_id in comuna:
            shape_ex = sf.shape(c_id)
            x_lon = np.zeros((len(shape_ex.points),1))
            y_lat = np.zeros((len(shape_ex.points),1))
            for ip in range(len(shape_ex.points)):
                x_lon[ip] = shape_ex.points[ip][0]
                y_lat[ip] = shape_ex.points[ip][1]
            ax.fill(x_lon,y_lat,fill_color)
            # annotations
            if annotate:
                x0 = np.mean(x_lon)
                y0 = np.mean(y_lat)
                plt.text(x0,y0,c_id,fontsize=10)
            
    # highlight borders
    if fill_comuna != -1:
        for c_id in comuna_fill:
            shape_ex = sf.shape(c_id)
            x_lon = np.zeros((len(shape_ex.points),1))
            y_lat = np.zeros((len(shape_ex.points),1))
            for ip in range(len(shape_ex.points)):
                x_lon[ip] = shape_ex.points[ip][0]
                y_lat[ip] = shape_ex.points[ip][1]
            plt.plot(x_lon,y_lat,border_color,linewidth=3)

    # add limits
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)

    if save:
        fig.savefig(title)
    
    plt.show()
    
def calc_color(data, color='Blues'):
    # receives data, returns bins
    if color   == 1: color_sq = ['#dadaebFF','#bcbddcF0','#9e9ac8F0','#807dbaF0','#6a51a3F0','#54278fF0']; colors = 'Purples';
    elif color == 2: color_sq = ['#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8','#253494']; colors = 'YlGnBu';
    elif color == 3: color_sq = ['#f7f7f7','#d9d9d9','#bdbdbd','#969696','#636363','#252525']; colors = 'Greys';
    elif color == 9: color_sq = ['#ff0000','#ff0000','#ff0000','#ff0000','#ff0000','#ff0000']
    else:            color_sq = ['#ffffd4','#fee391','#fec44f','#fe9929','#d95f0e','#993404']; colors = 'YlOrBr';
    new_data, bins = pd.qcut(data, 6, retbins=True, labels=list(range(6)))
    color_ton = []
    for val in new_data:
        color_ton.append(color_sq[val]) 
    if color != 9:
        colors = sns.color_palette(colors, n_colors=6)
        sns.palplot(colors, 0.6)
    return color_ton, bins

def plot_map_fill_multiples_ids_tone(sf,
                                     title,
                                     comuna,  
                                     print_id,
                                     color_ton, 
                                     bins, 
                                     x_lim = None, 
                                     y_lim = None, 
                                     figsize = figsize,
                                     save=False):
        
    fig, ax = plt.subplots(figsize = figsize)
    fig.suptitle(title, fontsize=16)

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            x = [i[0] for i in shape.shape.points[i_start:i_end]]
            y = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(x, y, 'k')
            
    for id in comuna:
        shape_ex = sf.shape(id)
        x_lon = np.zeros((len(shape_ex.points),1))
        y_lat = np.zeros((len(shape_ex.points),1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        ax.fill(x_lon,y_lat,color_ton[comuna.index(id)])
        if print_id != False:
            x0 = np.mean(x_lon)
            y0 = np.mean(y_lat)
            plt.text(x0, y0, id, fontsize=10)
            
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)
        
    if save:
        fig.savefig(title)
        
    plt.show()
    
def conv_comuna(comuna):
    if comuna == 'estacion central': return 'estación central'
    elif comuna == 'nunoa': return 'ñuñoa'
    elif comuna == 'maipu': return 'maipú'
    elif comuna == 'san ramon': return 'san ramón'
    elif comuna == 'san joaquin': return 'san joaquín'
    elif comuna == 'conchali': return 'conchalí'
    elif comuna == 'penaflor': return 'peñaflor'
    elif comuna == 'san jose de maipo': return 'san josé de maipo'
    elif comuna == 'penalolen': return 'peñalolén'
    elif comuna == 'maria pinto': return 'maría pinto'
    elif comuna == 'curacavi': return 'curacaví'
    elif comuna == 'alhue': return 'alhué'    
    else: return comuna

def plot_comunas_data(sf,
                      title,
                      comunas,
                      data=None,
                      color=None,
                      print_id=False,
                      figsize=figsize
                     ):

    # plot map with selected comunes, using specific color
    color_ton, bins = calc_color(data, color)
    
    df = read_shapefile(sf)
    comuna_id = []
    for i in comunas:
        i = conv_comuna(i).upper()
        comuna_id.append(df[df.NOM_COMUNA == 
                            i.upper()].index.to_list()[0])
        
    plot_map_fill_multiples_ids_tone(sf, title, comuna_id, 
                                     print_id, 
                                     color_ton, 
                                     bins, 
                                     x_lim = None, 
                                     y_lim = None, 
                                     figsize = figsize)