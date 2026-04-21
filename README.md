# chess

## Contributing

Ensure you have Python 3.14.2 or higher.
```
python -m venv .venv
(.venv) source .venv/bin/activate
(.venv) pip install -r requirements.txt
```

If you write code that requires new dependencies not tracked by the `requirements.txt`, update it with
```
(.venv) pip freeze > requirements.txt
```

## Usage

Run the `chess_engine` module with
```
(.venv) python -m chess_engine
```

Run submodules (e.g. `chess_engine/foo.py`) with
```
(.venv) python -m chess_engine.foo
```
