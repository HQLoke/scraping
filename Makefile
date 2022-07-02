# Implicit variables
PY      = python
PYFLAGS = -W ignore

# Source codes
SRCS = 

# Targets
MAIN = main.py

all:
	@$(PY) $(PYFLAGS) $(MAIN)

test:
	@$(PY) $(PYFLAGS) ./test/test.py

.PHONY: test