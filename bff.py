import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def p_to_asterisk(p):
    """ 
    Convert p-values to appropriate text marker: **, *, +, n.s., etc. (Psychology convention)
    **** One datapoint at a time.
    
    p >= 0.10 : n.s.
    0.10 >= p > 0.05 : +
    0.05 >= p > 0.01 : *
    0.01 >= p > 0.001 : **
    0.001 >= p : ***
    """
    p_str  = ["$*$$*$$*$", "$*$$*$", "$*$", "$\dagger$", "n.s."]
    p_bins = [0.001, 0.01, 0.05, 0.10]
    return p_str[np.digitize(p, p_bins)] 

def barplot_annotate_brackets(ax, num1, num2, pval, datahandles, dh=.05, barh=.05, fs=None, maxasterix=None):
    """ 
    Annotate barplot with p-values.

    :param num1: number of left bar to put bracket over
    :param num2: number of right bar to put bracket over
    :param data: string to write or number for generating asterixes
    :param center: centers of all bars (like plt.bar() input)
    :param height: heights of all bars (like plt.bar() input)
    :param yerr: yerrs of all bars (like plt.bar() input)
    :param dh: height offset over bar / bar + yerr in axes coordinates (0 to 1)
    :param barh: bar height in axes coordinates (0 to 1)
    :param fs: font size
    :param maxasterix: maximum number of asterixes to write (for very small p-values)
    """

    text = p_to_asterisk(pval)
    
    center = np.mean(datahandles, axis=1)[:,0]
    height = np.mean(datahandles, axis=1)[:,1]
    yerr = datahandles[:,-1,-1] - height

    lx, ly = center[num1], height[num1]
    rx, ry = center[num2], height[num2]

    if yerr is not None:
        ly += yerr[num1]
        ry += yerr[num2]

    ax_y0, ax_y1 = ax.get_ylim()
    dh *= (ax_y1 - ax_y0)
    barh *= 0 ##(ax_y1 - ax_y0)

    y = max(ly, ry) + dh

    barx = [lx, lx, rx, rx]
    bary = [y, y+barh, y+barh, y]
    mid = ((lx+rx)/2, y+barh)

    ax.plot(barx, bary, c='black')

    kwargs = dict(ha='center', va='bottom')
    if fs is not None:
        kwargs['fontsize'] = fs

    ax.text(*mid, text, **kwargs)
    
def panellabel(ax, lbl, fsz=16, title=None):
    ax.text(0, 1.15 if title else 1.05, lbl, fontsize=fsz, va='bottom', ha='left', transform=ax.transAxes)
    if title:
        ax.set_title(title)