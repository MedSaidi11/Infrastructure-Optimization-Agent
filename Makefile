.PHONY: help install run

help:
	@echo "Infrastructure Analysis - Makefile"
	@echo "=================================="
	@echo "install    - Install dependencies"
	@echo "run        - Start server + run analysis"

install:
	uv sync

run:
	uv run python mcp_server.py & sleep 3 && uv run python main.py
