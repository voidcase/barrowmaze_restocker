plainify:
	# [ -d ./tables/plain ] || mkdir ./tables/plain;
	for i in ./tables/rot13/*; do
		tr 'a-zA-Z' 'n-za-mN-ZA-M' < $i > ./tables/plain/$(basename $i);
		done;

build-exe:
	docker run -it --user $(id -u):$(id -g) -v $(pwd):/src kicsikrumpli/wine-pyinstaller --clean --onefile barrowmaze_control_panel.py
	echo done!

build-elf:
	pyinstaller --clean --onefile barrowmaze_control_panel.py

