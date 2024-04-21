# `zoink`

## Install

```bash
pipx install zoink
```

## Usage

```
Usage: zoink [OPTIONS] [APP_NAME]

Options:
  --duration TEXT  Duration to keep the application in focus. Format: 1h2m,
                   20m, 30s etc.
  --delay FLOAT    Delay between checks for focus change.
  --help           Show this message and exit.
```

`APP_NAME` is optional. If not provided, the application will be chosen based on the currently focused window after a delay of 3 seconds.