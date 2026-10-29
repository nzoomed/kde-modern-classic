# KDE Modern Classic - build, check, install.  GNU make and Python 3 (standard library only).
#
#   make build         redraw the theme from src/ into KDE-Modern-Classic/
#   make test          check the theme folder (links, names, SVG problems, index.theme)
#   make check-build   rebuild into build/ and confirm it matches KDE-Modern-Classic/ exactly
#   make install       install for this user (~/.local/share/icons); PREFIX=/usr for all users (needs root)
#   make uninstall     remove it again
#   make dist          KDE-Modern-Classic-YYYYMMDD.tar.gz, ready for the KDE Store
#   make addon-generic-browser   build the optional Firefox add-on (addon-kit/generic-browser)

THEME   := KDE-Modern-Classic
PYTHON  ?= python3
PREFIX  ?= $(HOME)/.local
ICONDIR := $(DESTDIR)$(PREFIX)/share/icons
VERSION := $(shell date +%Y%m%d)
SIZES   := scalable 16x16 22x22

.PHONY: all build test check-build install uninstall dist addon-generic-browser clean

all: test

build:
	rm -rf build/new
	cd src && $(PYTHON) gen.py ../build/new
	for d in $(SIZES); do rm -rf $(THEME)/$$d; cp -a build/new/$$d $(THEME)/; done
	cp build/new/index.theme $(THEME)/
	$(PYTHON) tools/check_theme.py $(THEME)

test:
	$(PYTHON) tools/check_theme.py $(THEME)

check-build:
	rm -rf build/check
	cd src && $(PYTHON) gen.py ../build/check > /dev/null
	$(PYTHON) tools/compare_builds.py $(THEME) build/check
	@echo "The committed theme matches the source."

install:
	mkdir -p "$(ICONDIR)"
	rm -rf "$(ICONDIR)/$(THEME)"
	cp -a $(THEME) "$(ICONDIR)/"
	rm -f "$(HOME)/.cache/icon-cache.kcache"
	@echo "Installed to $(ICONDIR)/$(THEME). Choose it in System Settings > Colours & Themes > Icons."

uninstall:
	rm -rf "$(ICONDIR)/$(THEME)"
	rm -f "$(HOME)/.cache/icon-cache.kcache"

dist: test
	tar -czf $(THEME)-$(VERSION).tar.gz $(THEME)
	@echo "Wrote $(THEME)-$(VERSION).tar.gz"

addon-generic-browser:
	$(PYTHON) addon-kit/generic-browser/make_icon.py
	$(PYTHON) addon-kit/make_addon.py addon-kit/generic-browser

clean:
	rm -rf build $(THEME)-*.tar.gz
	find . -name __pycache__ -prune -exec rm -rf {} +
