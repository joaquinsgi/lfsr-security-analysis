# LFSR Security Analysis

Security analysis and optimization of LFSR-based pseudorandom sequence generators for stream cipher cryptosystems.

**Bachelor's Thesis — Grado en Ingeniería Informática**  
Universidad de Granada · ETSIIT

---

## Project structure

```
src/
├── lfsr.py                  # Core LFSR implementation
├── berlekamp_massey.py      # Berlekamp-Massey algorithm
├── tests_nist/              # NIST SP 800-22 statistical tests
│   ├── monobit.py
│   ├── block_frequency.py
│   ├── runs.py
│   ├── binary_matrix.py
│   ├── maurer.py
│   ├── serial.py
│   └── linear_complexity.py
├── generators/              # LFSR-based generators
│   ├── shrinking.py
│   ├── self_shrinking.py
│   ├── geffe.py
│   └── alternating_step.py
└── analysis/
    ├── linear_complexity.py # LC profile and metrics
    └── plots.py             # Visualizations

results/                     # Output data from experiments

docs/                        # LaTeX memory (Spanish)
└── chapters/

tests/                       # Unit tests
```

## Requirements

```bash
pip install -r requirements.txt
```

## How to run

Generate a sequence and run all NIST tests:

```bash
python src/lfsr.py
```

Run a specific generator:

```bash
python src/generators/shrinking.py
```

Run unit tests:

```bash
python -m pytest tests/
```

## Language conventions

- Source code, comments, commit messages: **English**
- Academic memory (`docs/`): **Spanish**
