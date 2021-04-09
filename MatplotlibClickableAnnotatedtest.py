
import numpy as np
import matplotlib.pyplot as plt


#xy dummy data

x = np.linspace(0, 10, 100)
y = np.exp(x**0.5) * np.sin(5*x)

fig, ax = plt.subplots()
ax.set_title('Clickable Graph test')

line = ax.plot(x, y, picker=True, pickradius=5)

#set up for annotation visual
annot = ax.annotate("", xy=(0,0), xytext=(-40,40),textcoords="offset points",
                    bbox=dict(boxstyle='round4', fc='linen',ec='k',lw=1),
                    arrowprops=dict(arrowstyle='-|>'))
annot.set_visible(False)

#pick point/annotate graph function
def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    xpoints = xdata[ind]
    ypoints = ydata[ind]
    first_xpoint=xpoints[0]
    first_ypoint=ypoints[0]

    annot.xy = (first_xpoint, first_ypoint)
    text = "({:.2g}, {:.2g})".format(first_xpoint, first_ypoint)
    annot.set_text(text)
    annot.set_visible(True)
    fig.canvas.draw()

fig.canvas.mpl_connect('pick_event', onpick)

plt.show()
