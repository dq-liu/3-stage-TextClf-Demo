#!/usr/bin/python3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import matplotlib.patches as mpatches
import seaborn as sns

import mpld4
from mpld4 import plugins
from mpld4._server import serve
import pickle
import numpy as np

import pandas as pd
import random
import scipy.stats as stats
from sklearn.manifold import TSNE


def get_fold_idx(n, minibatch_size):
    np.random.seed(201808)
    idx_list = np.arange(n, dtype="int32")
    np.random.shuffle(idx_list)
    minibatches = []
    minibatch_start = 0
    for i in range(n // minibatch_size):
        minibatches.append(idx_list[minibatch_start:minibatch_start + minibatch_size])
        minibatch_start += minibatch_size
    return zip(range(len(minibatches)), minibatches)

class ClickInfo(mpld4.plugins.PluginBase):
    
    JAVASCRIPT = """
    mpld3.register_plugin("clickinfo", ClickInfo);
    ClickInfo.prototype = Object.create(mpld3.Plugin.prototype);
    ClickInfo.prototype.constructor = ClickInfo;
    ClickInfo.prototype.requiredProps = ["id", "urls"];
    
    function ClickInfo(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };
    
    function setIframeSrc(id, url){
        document.getElementById(id).src = url;
    };

    ClickInfo.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);
        urls = this.props.urls;
        obj.elements().on("mousedown", 
                          function(d, i){
                              setIframeSrc('ifrm', urls[i])
                          });
    }
    """
    
    def __init__(self, points, urls):
        self.points = points
        self.urls = urls
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None
        self.dict_ = {"type": "clickinfo",
                      "id": mpld4.utils.get_id(points, suffix),    # suffix = None
                      "urls": urls}     
        

def main(user, foldnumber):
    idx_ = list(fold_idx)[foldnumber][1]
    x_ = x_proj[idx_]
    y_ = y[idx_]
    y_sump_ = y_sump[idx_]
    noteid_ = noteid[idx_]
    
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    
    colors = ['red', 'orange', 'gold', 'green', 'blue', 'aqua', 'purple', 'pink', 'darkkhaki', 'black', 'violet', 'lightgray']
    palette = np.array(sns.color_palette(colors))
    points = ax.scatter(x_[:,0], x_[:,1], lw=1, s=y_sump_, c=palette[y_.astype(np.int)], edgecolors='k', alpha=0.8)

    plt.xlim(-65, 65)
    plt.ylim(-65, 65)
    ax.axis('off')
    ax.axis('tight')
    
    legend_dict = {'power of attorney':'red', 'lives with':'orange', 'family':'gold', 'comfort':'green',
                   'independence':'blue', 'be with family':'aqua', 'disabled':'purple', 'belief':'pink',
                   'resuscitate':'darkkhaki', 'aggressive':'black', 'code status':'violet', '*multi label': 'lightgray'}
    patchList = [mpatches.Patch(color=legend_dict[key], label=key) for key in legend_dict]
    plt.legend(handles=patchList, prop={'size':10}, framealpha=0.8,
               handlelength=1, borderaxespad=0)

    urls = ['http://pace-ql82pw3.dhe.duke.edu:5000/ajsjalaksneeeoeoa28474/'+str(user)+'/'+str(i) for i in noteid_]
    ports = {'casarett':8892, 'childers':8893, 'griffith':8894, 'lowe':8896, 'kim':8895, 'mumm':8897, 'test':8898}

    plugins.connect(fig, ClickInfo(points, urls))
    mpld4.show(ip='pace-ql82pw3.dhe.duke.edu', port=ports[user])


if __name__ == '__main__':
    x_proj   = pickle.load(open('x_proj_100k.p', 'rb'), encoding='latin1')
    y        = pickle.load(open('y_100k.p', 'rb'), encoding='latin1')
    y_sump   = pickle.load(open('y_sump_100k.p', 'rb'), encoding='latin1')
    noteid   = pickle.load(open('noteid_100k.p', 'rb'), encoding='latin1')
    fold_idx = get_fold_idx(len(y), 5000)
    user     = 'test'
    main(user, 6)