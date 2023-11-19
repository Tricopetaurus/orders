# Orders

Given a csv with couriers with N stops, display
what position they'll be in as they make their
way to their destinations.


## Demo

![Demo](./docs/demo.gif)

## Install

Create and activate python virtual environment,
then install the required dependencies

```bash
$ python -m venv ./venv
$ source ./venv/bin/activate
$ pip -r ./requirements.txt
$ pip install -e .
```

## Run

```bash
$ python -m orders ./orders.csv
```

## TODO Notes

### Add a Legend

### Accept slider / annotations as cmdline args

### Don't use Matplotlib

Matplotlib is great until you need to bring in PyQT5,
Might refactor to use bokeh as that leans on web.
The frustrating thing with bokeh is the callbacks are in javascript
