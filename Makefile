#!/usr/bin/make -f
# ==============================================================================
# Makefile - Taller de arboles, recorridos y complejidad computacional
# Integrantes: Dylan Torres - Juan Gomez - Javier Rosero
# Asignatura: Lenguajes de Programacion y Traduccion
# ==============================================================================

PYTHON ?= python3

.PHONY: all run test clean help

all: run

run:
	@$(PYTHON) main.py

test: run

clean:
	@echo "Limpiando archivos temporales y caches..."
	@rm -rf __pycache__ *.pyc
	@echo "Limpieza completada."

help:
	@echo "Comandos disponibles:"
	@echo "  make       - Ejecuta las pruebas completas de los cinco puntos"
	@echo "  make run   - Mismo comportamiento que 'make'"
	@echo "  make test  - Mismo comportamiento que 'make'"
	@echo "  make clean - Elimina archivos compilados temporales de Python"
