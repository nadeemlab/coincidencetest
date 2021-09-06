#!/usr/bin/env python3
import re
import base64

page = open('layout.html').read()

style_css = open('style.css', 'rt').read()
page = page.replace('{{style.css}}', style_css)

utilities_js = open('utilities.js', 'rt').read()
page = page.replace('{{utilities.js}}', utilities_js)

question_mark = open('questionmark.svg', 'rb').read()
question_mark = str(base64.b64encode(question_mark), 'utf-8')
page = page.replace('{{question-icon-base64}}', question_mark)

loader = open('loader.svg', 'rb').read()
loader = str(base64.b64encode(loader), 'utf-8')
page = page.replace('{{loader-icon-base64}}', loader)

example_tsv = open('multiplexed_1500.tsv', 'rb').read()
example_tsv = str(base64.b64encode(example_tsv), 'utf-8')
data_uri = 'data: text/tab-separated-values;base64,' + example_tsv
page = page.replace('{{multiplexed_1500.tsv}}', data_uri)

worker = open('_worker.js').read()
coincidencetest_js = open('coincidencetest.js', 'rt').read()
worker = worker.replace('{{coincidencetest.js}}', coincidencetest_js)
fca_js = open('fca.js', 'rt').read()
worker = worker.replace('{{fca.js}}', fca_js)
open('worker.js', 'wt').write(worker)

open('index.html', 'w').write(page)
