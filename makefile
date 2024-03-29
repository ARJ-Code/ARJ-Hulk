.PHONY: dev
dev:
	python3 src/main.py

.PHONY: test
test:
	python3 src/test.py

.PHONY: build
build:
	python3 src/build.py


.PHONY: compile
compile:
	gcc -o cache/main cache/main.c -lm && ./cache/main 

