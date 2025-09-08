# Jarvis Makefile - Cross-platform
UV_VERSION := 0.8.13

.PHONY: install run check-uv activate

# Detect OS
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    PYTHON := python
    VENV_ACTIVATE := .venv\\Scripts\\activate
else
    DETECTED_OS := $(shell uname -s)
    PYTHON := python3
    VENV_ACTIVATE := source .venv/bin/activate
endif

check-uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv $(UV_VERSION)..."; \
		if [ "$(DETECTED_OS)" = "Windows" ]; then \
			powershell -Command "irm https://astral.sh/uv/$(UV_VERSION)/install.ps1 | iex"; \
		else \
			curl -LsSf https://astral.sh/uv/$(UV_VERSION)/install.sh | sh; \
		fi; \
		echo "Please restart your shell or add uv to PATH"; \
		exit 1; \
	else \
		echo "uv is already installed"; \
	fi

install: check-uv
	uv venv && uv pip install -r requirements.txt

activate:
	@echo "To activate virtual environment:"
	@echo "  $(VENV_ACTIVATE)"

run:
	$(PYTHON) main.py