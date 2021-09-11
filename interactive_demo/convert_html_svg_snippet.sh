#!/bin/bash
wkhtmltoimage --margin-top 0 --margin-bottom 0  figure.html figure.svg
wkhtmltopdf --margin-top 0 --margin-bottom 0 figure.html figure.pdf

