#!/usr/bin/env python

import csv
from scale import Scale
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []


thescale = Scale(10202)

starttime = time.time()

old_time = 0.0
old_weight = 0.0

with open('output.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(["deltatime","weight"])

    def animate(i, xs, ys):
        # Add x and y to lists
        global old_time
        global old_weight

        time_last_received, weight = thescale.return_last_weight()
        if time_last_received > old_time and weight != old_weight:
            old_time = time_last_received
            old_weight = weight

            print('got new data', time_last_received, weight)
            deltatime = time_last_received - starttime

            xs.append(deltatime)
            ys.append(weight) # Adds kg
            datawriter.writerow([deltatime,weight])

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
        else:
            return

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
    plt.show()

if __name__ == '__main__':
    main()