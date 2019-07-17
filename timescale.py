#!/usr/bin/env python

import csv
from scale import Scale
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []


thescale = Scale('192.168.1.4','4001')

with open('output.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(["timenow","weightnow"])
    # This function is called periodically from FuncAnimation
    def animate(i, xs, ys):
        # Add x and y to lists
        timenow = dt.datetime.now().strftime('%H:%M:%S')
        
        scaledata = thescale.lastdata()
        weightnow = scaledata[2]
        
        xs.append(timenow)
        ys.append(weightnow) # Adds kg
        
        print(timenow,weightnow)
        datawriter.writerow([timenow,weightnow])

        # Limit x and y lists to 120 items, 1 sec per item
        xs = xs[-120:]
        ys = ys[-120:]

        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Weight kg over Time')
        plt.ylabel('Weight kg')

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)

    plt.show()







if __name__ == '__main__':
    main()