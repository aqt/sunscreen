# Sunscreen

Automatically adjust your monitors' brightness based on the surrounding light.

# Overview

- **Server**: Runs on an MCU and provides light level readings via a serial interface over USB
- **Client**: Runs on your computer, periodically polling the server for the current light level and adjusting the monitor's brightness accordingly

Refer to their respective README.md for more information.

# Hardware
- CH552 board
- Photoresistor
- 1K ohm resistor

## Wiring diagram
```mermaid
graph LR
	subgraph " "
		ldr[Photoresistor]
		edge[ ]
		r[1k resistor]
	end
	
	subgraph " "
		p10["P1.0 (5v)"]
		p14["P1.4 (read)"]
		gnd[GND]
	end

	ldr --- p10
	edge --- ldr
	edge --- p14
	edge --- r

	r --- gnd
```