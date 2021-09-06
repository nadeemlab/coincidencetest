#!/usr/bin/env python3
import re
import base64

page = open('layout.html').read()

style_css = open('style.css', 'rt').read()
page = page.replace('{{style.css}}', style_css)

coincidencetest_js = open('coincidencetest.js', 'rt').read()
page = page.replace('{{coincidencetest.js}}', coincidencetest_js)

fca_js = open('fca.js', 'rt').read()
page = page.replace('{{fca.js}}', fca_js)

utilities_js = open('utilities.js', 'rt').read()
page = page.replace('{{utilities.js}}', utilities_js)

question_mark = open('questionmark.svg', 'rb').read()
question_mark = str(base64.b64encode(question_mark), 'utf-8')
page = page.replace('{{question-icon-base64}}', question_mark)

loader = open('loader.svg', 'rb').read()
loader = str(base64.b64encode(loader), 'utf-8')
page = page.replace('{{loader-icon-base64}}', loader)

open('index.html', 'w').write(page)
