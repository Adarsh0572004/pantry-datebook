# Pantry Datebook

List pantry batches in earliest-expiry order.

## Quick start

Use Python 3.10 or newer. All dependencies are in the standard library.

```sh
python app.py store Rice 2027-04-12
python app.py store Oats 2027-02-10
python app.py list
```

The example output includes `2027-02-10 | Oats`.

Records are saved in `pantry-datebook.sqlite3` in the working directory. Use `--db PATH` before the command to choose another database. Run `python app.py --help` for the available options.
