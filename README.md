Libstripper
===========
If you only use bootstrap buttons, why are you loading all 7000 lines? Libstripper is a commandline tool that strips away unused css from a library.

Installation
============
Put it anywhere you want !

Usage
======
You have two options when using libstripper

- You can specify a css library and html file like so

```python libstripper.py --html /path/to/html --css /path/to/css```

- Or you can speicfy a css library and a directory containing html files

```python libstripper.py --html /path/to/html --dir /path/to/directory```

Your stripped css file will be stored in the same directory as your css file but with -stripped appended. For instance bootstrap.css becomes bootstrap-stripped.css.

