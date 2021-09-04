#!/usr/bin/env python3
import re
import base64

layout = open('layout.html').read()

style_css = open('style.css').read()
page = re.sub('{{style.css}}', style_css, layout)

question_mark = open('questionmark.svg', 'rb').read()
question_mark = str(base64.b64encode(question_mark), 'utf-8')
page = re.sub('{{question-icon-base64}}', question_mark, page)

loader = open('loader.svg', 'rb').read()
loader = str(base64.b64encode(loader), 'utf-8')
page = re.sub('{{loader-icon-base64}}', loader, page)

open('index.html', 'w').write(page)
