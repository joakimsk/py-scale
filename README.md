# scale

A module for interfacing with scales. Tested on OS X High Sierra with Python 3.7.

Uses a thread to do work without blocking, need to poll data.

Line identification not optimal, drops maybe 15% of lines.

# Setup of DINI DFWLKI panel RS232 output
See page 41 in [TECH_MAN_ENG_DFW_v4.pdf](http://www.diniargeo.by/Downloads/INDIKATORY/Series_DFW/TECH_MAN_ENG_DFW_v4.pdf) for description of communication strings. See page 12 and onwards for Serial Port configuration.

My panel diverges in the settings of the menu, so you may need to map the menus out on paper and try your way around. Decimals may very well also be configurable.

The extended string format, according to the manual:
01ST,1, 0.0,PT 20.8, 0,kg<CR><LF>
The actual extended string I receive is 44 bytes long:
1,ST,     0.000,       0.000,         0,kg<CR><LF>

The short string format, according to the manual:
01ST,GS, 0.0,kg<CR><LF>
The actual short string I receive is 20 bytes long:
ST,GS,   0.000,kg<CR><LF>

# Setup of Moxa NPORT 5110A RS232-ETH Converter
Manual [NPort_5100A_Series_Users_Manual_v2.pdf](http://support.elmark.com.pl/moxa/products/Serwery_portow_szeregowych/NPort_P5150A/manual/NPort_5100A_Series_Users_Manual_v2.pdf) 

Remember to upgrade to latest firmware, a lot of faults gets fixed.

You can either use UDP or TCP Client / Server Mode on the converter. I recommend UDP since traffic will flow one way, and I prioritize in-time delivery of data more than accuracy.

The <CR><LF> two-byte delimiter is represented by \x0d\x0a in hexadecimal, this can be used in "Data Packing" settings of the converter.

# Tuning for best performance using scalecalib.py
To check communication performance, use the simple display program, and record using a video. Count frames from weight increases on the panel, to when weight is equal in display program and STABLE is indicated (First parameter is ST).

In my case, the video recorded was taken with 25 frames per second, and I counted 29 frames from initial weight is detected by scale untill display program shows same weight. 29/25=1.16 sec, more or less.

You can adjust baud rates and other settings to try to get better performance.

# Windows Firewall
If you have to deal with Windows, remember that the firewall is likely blocking your UDP packets. Add a rule to allow.

# Verified supported scales
ScaleIT PSX30 with DINI DFWLKI panel and DINI PBQI30 base and Moxa NPORT 5110A RS232-ETH Converter
