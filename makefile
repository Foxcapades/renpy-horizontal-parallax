VERSION := $(shell grep 'define config.version' game/options.rpy | sed 's/.\+"\(.\+\)"/\1/')
FEATURE := $(shell grep 'define config.version' game/options.rpy | sed 's/.\+"\(.\+\)"/\1/;s/\([0-9]\+\.[0-9]\+\).\+/\1.0/')

SLIM_ZIP_NAME := .build/ps-slim-$(VERSION).zip
FULL_ZIP_NAME := .build/ps-project-$(VERSION).zip

.PHONY: default
default:
	@echo "What are you doing?"


.PHONY: clean
clean:
	@echo "Cleaning directory."
	@find . -name '*.rpyc' -o -name '*.rpyb' -o -name '*.rpymc' | xargs -I'{}' rm '{}'


.PHONY: release
release: pre-release build-base-project-zip build-slim-zip build-distributions


.PHONY: pre-release
pre-release: clean
	@rm -rf .build errors.txt log.txt traceback.txt


.PHONY: build-base-project-zip
build-base-project-zip: clean
	@mkdir -p .build
	@rm -f "$(FULL_ZIP_NAME)"
	@cp license parallax-scroll-license
	@cp credits.txt parallax-scroll-credits.txt
	@zip -r "$(FULL_ZIP_NAME)" game parallax-scroll-license parallax-scroll-credits.txt -x game/saves/**\* -x game/cache/**\*
	@rm parallax-scroll-license parallax-scroll-credits.txt


.PHONY: build-slim-zip
build-slim-zip: clean
	@mkdir -p .build
	@rm -f "$(SLIM_ZIP_NAME)"
	@cp license parallax-scroll-license
	@zip -r "$(SLIM_ZIP_NAME)" game/lib/fxcpds/parallax_scroll parallax-scroll-license
	@rm parallax-scroll-license


.PHONY: build-distributions
build-distributions: clean
	@mkdir -p .build
	@renpy-8.1.1 /opt/renpy/8.1.1/launcher distribute . --package=pc --dest=.build
	@renpy-8.1.1 /opt/renpy/8.1.1/launcher distribute . --package=mac --dest=.build
	@renpy-8.1.1 /opt/renpy/8.1.1/launcher distribute . --package=linux --dest=.build


.PHONY: docs
docs:
	@mkdir -p docs/versions/$(FEATURE)
	@asciidoctor -b html5 -o docs/index.html -a revnumber=$(FEATURE) docs/index.adoc
	@asciidoctor -b html5 -o docs/versions/$(FEATURE)/index.html -a revnumber=$(FEATURE) docs/reference/index.adoc
	@asciidoctor -b html5 -o docs/versions/$(FEATURE)/tutorial.html -a revnumber=$(FEATURE) docs/reference/tutorial.adoc