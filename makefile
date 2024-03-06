.PHONY: dev
dev:
	python src/main.py

.PHONY: prove
prove:
	python src/prove.py

.PHONY: test
test:
	python src/test.py