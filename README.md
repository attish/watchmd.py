watchmd.py -- instant single-file Markdown server
=================================================

Purpose
-------

Tracks and displays a live rendering of a Markdown text file in a web
browser.

Usage
-----

    $ python watchmd.py <port> <file>

Notes
-----

Required Python packages:

* web.py
* markdown

Uses the long poll variant of HTTP Push to implement live refresh of
content when the source file changes.

