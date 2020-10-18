UNAME := $(shell uname)

ifeq ($(UNAME), Linux)
	SOURCE = libfractal.so
	TARGET = _fractal.so
else ifeq ($(UNAME), Darwin)
	SOURCE = libfractal.dylib
	TARGET = _fractal.so
else
	SOURCE = libfractal.dll
	TARGET = _fractal.pyd
endif

build:
	cargo build
	cp target/debug/$(SOURCE) fractal/$(TARGET)

release:
	cargo build --release
	cp target/release/$(SOURCE) fractal/$(TARGET)

clean:
	cargo clean
	rm -f fractal/$(TARGET)

.PHONY: build release clean
