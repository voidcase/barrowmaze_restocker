build-exe:
	docker run -it --user $(id -u):$(id -g) -v $(pwd):/src kicsikrumpli/wine-pyinstaller --clean --onefile barrowmaze_control_panel.py
	echo done!

build:
	pyinstaller --clean --add-data ./tables:tables barrowmaze_control_panel.py

