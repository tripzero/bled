EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:blelight
LIBS:led-rfduino-rgb-cache
EELAYER 27 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "24 feb 2015"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L R R4
U 1 1 54E9181E
P 6300 2250
F 0 "R4" V 6380 2250 40  0000 C CNN
F 1 "3ohm 1W" V 6307 2251 40  0000 C CNN
F 2 "~" V 6230 2250 30  0000 C CNN
F 3 "~" H 6300 2250 30  0000 C CNN
	1    6300 2250
	1    0    0    -1  
$EndComp
$Comp
L RFDUINO BLE1
U 1 1 54E92802
P 3250 1500
F 0 "BLE1" H 3250 900 60  0000 C CNN
F 1 "RFDUINO" H 3250 2200 60  0000 C CNN
F 2 "" H 3250 1500 60  0000 C CNN
F 3 "" H 3250 1500 60  0000 C CNN
	1    3250 1500
	1    0    0    -1  
$EndComp
Wire Wire Line
	4150 2800 4400 2800
Wire Wire Line
	4200 1800 4600 2300
Wire Wire Line
	4300 1700 4600 2000
$Comp
L R R1
U 1 1 54E92872
P 4400 3050
F 0 "R1" V 4480 3050 40  0000 C CNN
F 1 "10k" V 4407 3051 40  0000 C CNN
F 2 "~" V 4330 3050 30  0000 C CNN
F 3 "~" H 4400 3050 30  0000 C CNN
	1    4400 3050
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 54E928A6
P 4950 3050
F 0 "R2" V 5030 3050 40  0000 C CNN
F 1 "10k" V 4957 3051 40  0000 C CNN
F 2 "~" V 4880 3050 30  0000 C CNN
F 3 "~" H 4950 3050 30  0000 C CNN
	1    4950 3050
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 54E928AC
P 5500 3050
F 0 "R3" V 5580 3050 40  0000 C CNN
F 1 "10k" V 5507 3051 40  0000 C CNN
F 2 "~" V 5430 3050 30  0000 C CNN
F 3 "~" H 5500 3050 30  0000 C CNN
	1    5500 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	1800 700  1800 3300
Wire Wire Line
	1800 3300 6050 3300
Connection ~ 6050 3300
Wire Wire Line
	6300 3300 6300 2500
$Comp
L LED D3
U 1 1 54E92923
P 6000 1400
F 0 "D3" H 6000 1500 50  0000 C CNN
F 1 "LED" H 6000 1300 50  0000 C CNN
F 2 "~" H 6000 1400 60  0000 C CNN
F 3 "~" H 6000 1400 60  0000 C CNN
	1    6000 1400
	-1   0    0    1   
$EndComp
$Comp
L LED D2
U 1 1 54E92930
P 5450 1600
F 0 "D2" H 5450 1700 50  0000 C CNN
F 1 "LED" H 5450 1500 50  0000 C CNN
F 2 "~" H 5450 1600 60  0000 C CNN
F 3 "~" H 5450 1600 60  0000 C CNN
	1    5450 1600
	-1   0    0    1   
$EndComp
$Comp
L LED D1
U 1 1 54E92936
P 4900 1800
F 0 "D1" H 4900 1900 50  0000 C CNN
F 1 "LED" H 4900 1700 50  0000 C CNN
F 2 "~" H 4900 1800 60  0000 C CNN
F 3 "~" H 4900 1800 60  0000 C CNN
	1    4900 1800
	-1   0    0    1   
$EndComp
Wire Wire Line
	6300 1400 6200 1400
Wire Wire Line
	6300 1600 5650 1600
Connection ~ 6300 1600
Wire Wire Line
	6300 1800 5100 1800
Connection ~ 6300 1800
Wire Wire Line
	4700 1800 4700 2600
Wire Wire Line
	5250 1600 5250 2600
Wire Wire Line
	5800 1400 5800 2600
Wire Wire Line
	5800 3000 5800 3300
Connection ~ 5800 3300
Wire Wire Line
	5250 3000 5250 3300
Connection ~ 5250 3300
Wire Wire Line
	4700 3000 4700 3300
Connection ~ 4700 3300
Wire Wire Line
	4600 2300 4950 2800
Wire Wire Line
	4600 2000 5500 2000
Wire Wire Line
	5500 2000 5500 2800
Connection ~ 6300 1400
Wire Wire Line
	2250 850  4300 850 
Wire Wire Line
	4300 700  1800 700 
$Comp
L R R5
U 1 1 54E92F15
P 2000 2350
F 0 "R5" V 2080 2350 40  0000 C CNN
F 1 "30k" V 2007 2351 40  0000 C CNN
F 2 "~" V 1930 2350 30  0000 C CNN
F 3 "~" H 2000 2350 30  0000 C CNN
	1    2000 2350
	1    0    0    -1  
$EndComp
Wire Wire Line
	2250 2600 2250 3300
Connection ~ 2250 3300
Wire Wire Line
	2450 1400 1800 1400
Connection ~ 1800 1400
Wire Wire Line
	2000 1500 2450 1500
Connection ~ 2000 1500
Wire Wire Line
	2250 2600 2000 2600
Wire Wire Line
	2000 2000 2000 2100
Wire Wire Line
	2000 1500 2250 850 
$Comp
L VR VR1
U 1 1 54E943F3
P 2000 1750
F 0 "VR1" V 2060 1704 40  0000 C TNN
F 1 "10Mohm" V 2000 1750 40  0000 C CNN
F 2 "~" H 2000 1750 60  0000 C CNN
F 3 "~" H 2000 1750 60  0000 C CNN
	1    2000 1750
	1    0    0    -1  
$EndComp
Wire Wire Line
	2250 2050 2000 2050
Connection ~ 2000 2050
Wire Wire Line
	4150 2800 4150 1900
Wire Wire Line
	4150 1900 4000 1900
Wire Wire Line
	4200 1800 4000 1800
Wire Wire Line
	4300 1700 4000 1700
$Comp
L POWER_REGULATOR P1
U 1 1 54E95C71
P 4750 1050
F 0 "P1" H 4750 1050 60  0000 C CNN
F 1 "POWER_REGULATOR" H 4800 1700 60  0000 C CNN
F 2 "" H 4750 1050 60  0000 C CNN
F 3 "" H 4750 1050 60  0000 C CNN
	1    4750 1050
	1    0    0    -1  
$EndComp
$Comp
L N_CHAN_MOSFET Q1
U 1 1 54E9683F
P 4600 2800
F 0 "Q1" H 4650 3000 60  0000 R CNN
F 1 "N_CHAN_MOSFET" H 5000 2550 60  0000 R CNN
F 2 "~" H 4600 2800 60  0000 C CNN
F 3 "~" H 4600 2800 60  0000 C CNN
	1    4600 2800
	1    0    0    -1  
$EndComp
$Comp
L N_CHAN_MOSFET Q2
U 1 1 54E9684E
P 5150 2800
F 0 "Q2" H 5200 3000 60  0000 R CNN
F 1 "N_CHAN_MOSFET" H 5550 2550 60  0000 R CNN
F 2 "~" H 5150 2800 60  0000 C CNN
F 3 "~" H 5150 2800 60  0000 C CNN
	1    5150 2800
	1    0    0    -1  
$EndComp
$Comp
L N_CHAN_MOSFET Q3
U 1 1 54E9685D
P 5700 2800
F 0 "Q3" H 5750 3000 60  0000 R CNN
F 1 "N_CHAN_MOSFET" H 6100 2550 60  0000 R CNN
F 2 "~" H 5700 2800 60  0000 C CNN
F 3 "~" H 5700 2800 60  0000 C CNN
	1    5700 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	5200 550  6750 550 
Wire Wire Line
	6750 550  6750 2500
Wire Wire Line
	6750 2500 6300 2500
Wire Wire Line
	6300 1400 6300 2000
Connection ~ 5500 3300
Connection ~ 4950 3300
Connection ~ 4400 3300
Wire Wire Line
	2250 2050 2250 2300
Wire Wire Line
	2250 2300 4300 2300
Wire Wire Line
	4300 2300 4300 1600
Wire Wire Line
	4300 1600 4000 1600
$Comp
L PWR_INPUT PWR1
U 1 1 54ECB369
P 6150 3700
F 0 "PWR1" H 6150 3450 60  0000 C CNN
F 1 "PWR_INPUT" H 6150 4050 60  0000 C CNN
F 2 "" H 6150 3700 60  0000 C CNN
F 3 "" H 6150 3700 60  0000 C CNN
	1    6150 3700
	0    1    1    0   
$EndComp
$Comp
L USB-PROGRAMMER USB1
U 1 1 54ECB74F
P 3150 2700
F 0 "USB1" H 3200 2150 60  0000 C CNN
F 1 "USB-PROGRAMMER" H 3150 3000 60  0000 C CNN
F 2 "" H 3150 2700 60  0000 C CNN
F 3 "" H 3150 2700 60  0000 C CNN
	1    3150 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	2750 2550 2450 2550
Wire Wire Line
	2450 2550 2450 3300
Connection ~ 2450 3300
Wire Wire Line
	2750 2650 2750 2500
Wire Wire Line
	2750 2500 2200 2500
Wire Wire Line
	2200 2500 2200 1500
Connection ~ 2200 1500
Wire Wire Line
	2450 1600 2300 1600
Wire Wire Line
	2300 1600 2300 2750
Wire Wire Line
	2300 2750 2750 2750
Wire Wire Line
	2750 2850 2350 2850
Wire Wire Line
	2350 2850 2350 1700
Wire Wire Line
	2350 1700 2450 1700
Wire Wire Line
	2550 2950 2750 2950
Wire Wire Line
	2550 1800 2550 2950
Wire Wire Line
	2550 1800 2450 1800
Wire Wire Line
	2750 3050 2650 3050
Wire Wire Line
	2650 3050 2650 2200
Wire Wire Line
	2650 2200 2400 2200
Wire Wire Line
	2400 2200 2400 1900
Wire Wire Line
	2400 1900 2450 1900
$EndSCHEMATC
