.PHONY: logos validate build serve clean

logos:
	bash ./scripts/fetch-logos.sh

validate:
	landscape2 validate data --data-file data.yml
	landscape2 validate settings --settings-file settings.yml
	landscape2 validate guide --guide-file guide.yml

build:
	bash ./scripts/build-landscape.sh
	bash ./scripts/postprocess-build.sh

serve:
	landscape2 serve --landscape-dir build

clean:
	rm -rf build .cache
