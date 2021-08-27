# pyprogress
A simple progress tracker for python which counts 'ticks', average time per tick, and then forecasts completion time including a confidence interval. Can be called in each iteration of a loop in order to track progress and estimate completion.

## Options
Required:
- Specify total number of expected ticks

Optional
- log: save a logfile of ticks and estimated times
- datestamp: specify a string to add to a logfile


## Example

>Initiate the tracker
>p = Progress(totalrows, datestamp = rundate, log=True)

>Tick the tracker
>progress.tick()

>Get a progress report
>print(progress.report())
