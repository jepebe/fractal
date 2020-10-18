build:
	cargo build
	cp target/debug/libfractal.dylib fractal/_fractal.so

release:
	cargo build --release
	cp target/release/libfractal.dylib fractal/_fractal.so

clean:
	cargo clean
	rm -f fractal/_fractal.so

.PHONY: build release clean
