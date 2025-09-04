## CLI

Schnelle Orchestrierung der Pipeline ohne UI.

### Installation

Aktiviere dein venv und stelle sicher, dass Abhaengigkeiten installiert sind.

### Nutzung

```bash
python cli.py run skizze1_vertical_split --ratio 50 --transparency 60 --seed 1 --out out.json --diagnostics diag.json --summary --snapshot snap.json
```

- `--ratio` 30..70
- `--transparency` 0..100
- `--seed` fuer deterministische Runs
- `--out` schreibt das finale Layout-JSON
- `--diagnostics` schreibt Metadaten (z.B. Zonenanzahl)
- `--summary` Druckt Kurzuebersicht
- `--snapshot` schreibt Layout als JSON-Snapshot

### Exitcodes

- 0: OK
- 1: Unerwarteter Fehler
- 2: Validation-Fehler


