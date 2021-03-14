

# BARROWMAZE RESTOCKER

An unofficial GUI/web application which automates the process of restocking previously visited rooms
while GMing Barrowmaze Complete. Turning multiple branching random table rolls into a single click.

## Barrowmaze?

It's a [very good megadungeon](https://www.youtube.com/watch?v=s5kmD5BufGU) for Old School D&D (specifically [Labyrinth Lord](https://www.drivethrurpg.com/product/64332/Labyrinth-Lord-Revised-Edition)).
[Buy it here!](https://www.drivethrurpg.com/product/139762/Barrowmaze-Complete)

# How to run it

It's still a bit rough around the edges, but here you go:

## as a GUI program:

requires tkinter

	python3 barrowmaze_control_panel.py

## as a web application:

requires flask and gunicorn

	gunicorn api:api
