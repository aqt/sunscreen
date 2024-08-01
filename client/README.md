# Client

- Samples the light several times and averages the result (mitigate temporary spikes)
- Fades the brightness changes to reduce intrusiveness

# Running instructions (Linux)

Note: I used Python 3.10 (because I haven't bothered updating yet). Otherwise no clue about required python version range.

## Setup
1. Create a virtual environment: `python3 -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## Run
`python3 main.py`

# Configuration parameters

## [general]
- `log_level`: Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
- `serial_port`: Board connection port

## [sampling]
- `samples`: Number of collected samples per cycle
- `sampling_interval`: Milliseconds between each samples

## [adjustment]
- `adjustment_interval`: Seconds between adjustments
- `forced_adjustment_delay`: Seconds until ignoring `minimum_lumi_step` and forcing adjustment. Set to `0` to disable
- `brightness_multiplier`: Factor that controls brightness scaling; `1` means brightness equals luminosity
- `fade_interval`: Milliseconds between fade steps, set to `0` to disable. If set too low your monitor may flicker as it struggles to keep up with updates
- `fade_step_size`: The change in brightness applied at each step
- `minimum_lumi_step`: Minimum luminosity difference for brightness adjustment. For reference, value range of luminosity is `0` to `100`