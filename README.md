# Word Connect

A small Vietnamese word-processing project that builds a graph of 2-word phrases and finds optimal word connections.

## Overview

This project reads a Vietnamese dictionary file and extracts all **2-word phrases**.  
Given a starting word, it finds all matching phrases and selects the ones that lead to the **fewest possible next words**.

This can be useful for:
- Word chain games (nối từ)
- Linguistic exploration
- Graph-based word analysis

## Files

- `noiTu.py` — main Python script
- `words.txt` — dictionary data (JSON lines format)

## Data Format

Each line in `words.txt` should look like:

```json
{"text": "ác quỷ", "source": ["hongocduc"]}
