all: release

.PHONY: release
release:
	zip terrain_eroder.zip terrain_eroder/*.py terrain_eroder/**/*.py
