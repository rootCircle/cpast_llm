init:
	rye sync # make sure poetry is installed
	rye run maturin develop

lint:
	rye lint
	rye run pyright # static type checking

lint-fix:
	rye lint --fix

run:
	rye run maturin develop --skip-install --quiet
	rye run python3 python/cpast_llm/main.py

fmt:
	rye fmt

test:
	rye test

precommit: lint fmt test
