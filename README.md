# scale

A module for interfacing with scales. Tested on OS X Mojave with Python 3.7.

Uses a thread to do work without blocking, need to poll data.

Line identification not optimal, drops maybe 15% of lines.

# Setup of DINI DFWLKI panel RS232 output
See page 41 in [TECH_MAN_ENG_DFW_v4.pdf](http://www.diniargeo.by/Downloads/INDIKATORY/Series_DFW/TECH_MAN_ENG_DFW_v4.pdf) for description of communication strings. See page 12 and onwards for Serial Port configuration.

Other manuals that may contain more information:
[Technical Manual DGT.pdf](https://www.vetek.se/Dynamics/Documents/72b4f220-71ff-4204-84e5-cc16a9755bad/Technical%20Manual%20DGT.pdf)
[DFWT_01.05_15.10_EN_T.pdf](http://www.diniargeo.by/Downloads/INDIKATORY/Series_DFW/DFWT_01.05_15.10_EN_T.pdf)
[DFW_03_14.11_EN_U.pdf](http://www.diniargeo.com/VisFile.aspx?file=MN2028&Name=pAFkSrb0pwzJyn2%2FCB1Ph4ijBObaTfkGAPxemIHIx6w%3D)

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

# Tuning for best performance using sot.py
To check communication performance, use the sot.py program, and record using a video. Count frames from weight increases on the panel, to when weight is equal in display program and on scale.

In default configuration, the scale was using "Filter level 3". The video recorded was taken with 25 frames per second, and I counted 29 frames from initial weight is detected by scale untill display program shows same weight. 29/25=1.16 sec, more or less. This is an averaging filter, so increased filtering means more samples must be taken before an average is calculated.

I modified scale filter to "Filter level 0", but the scale acted spurious, so I set it up to "Filter level 1". Now, I count only 1 frame between scale indicator and display program. 0.04 sec from scale display to computer is good.

You can adjust baud rates and other settings to try to get better performance. For me, it seems 19200 baud is good enough, and we get up to 28 messages per second. The communication between the converter and scale should be "as fast as possible", so 115200 should still be good, as long as communication does not break down due to noise. Anything below 19200 baud seems to throttle messages, leading to longer delays, and possibly filling up buffers somewhere.

There is no UI on sot.py, to reduce error-sources. Increase font size in terminal if you need.

# Windows Firewall
If you have to deal with Windows, remember that the firewall is likely blocking your UDP packets. Add a rule to allow.

# Verified supported scales
ScaleIT PSX30 with DINI DFWLKI panel and DINI PBQI30 base and Moxa NPORT 5110A RS232-ETH Converter
