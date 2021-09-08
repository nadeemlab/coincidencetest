#!/usr/bin/env python3

import coincidencetest
from coincidencetest import coincidencetest
from coincidencetest._coincidencetest import calculate_probability_of_multicoincidence

data = [
    [1,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,1,1,1],
    [0,0,1,0,1,1,0,0,1,1,0,1,1,0,0,1,0,1,1,1],
    [0,0,1,1,0,0,0,0,0,1,0,1,0,1,0,1,1,1,1,1],
    [0,1,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0,1,1,1],
]

def create_html(data):
    intersections = [
        i for i in range(len(data[0])) if all(row[i]==1 for row in data)
    ]

    style = '''
    body {
        font-family: sans-serif;
        font-size: 1.2em;
    }
    div.figdiv {
        text-align: center;
    }
    div.tableheatbounder {
        background-color: #eeeeee;
        display: inline-block;
        padding: 15px;
    }
    p.tabletitle {
        text-align: center;
    }
    p {
        text-align: center;
    }
    table.heat {
        border-spacing: 3px;
        padding: 10px;
        display: inline;
    }
    table.heat tr th {
        padding: 5px;
    }
    table.heat tr td {
        padding: 25px 10px 10px 25px;
        text-align: center;
    }

    table.heat tr td.zero {
        /* background: #F0FFFF; */
        background: #e9e3f8;
    }
    table.heat tr td.zero:hover {
        background: #cdbbf4;
    }

    table.heat tr td.one {
        /* background: #F08080; */
        background: #f25b24;
    }
    table.heat tr td.one:hover {
        background: #f6a476;
    }

    table.heat tr td.highlight {
        background: lightgray;
    }

    div.tablestatsbounder {
        background-color: #eeeeee;
        display: inline-block;
        padding: 15px;
    }

    table.stats {
        display: inline;
    }

    table.stats tr td.pvals {
        width: 20ch;
    }

    table.stats tr td {
        text-align: left;
        padding: 15px;
    }

    .numintersections {
        font-weight: bold;
    }

    .numintersections:hover {
        text-decoration: underline dotted;
        cursor: default;
    }

    #captiontext {
        padding: 0 30% 0 30%;
        text-align: left;
    }

    .pmetercontainer {
        border: 1px solid gray;
        width: 180px;
        height: 15px;
        display: inline-block;
    }

    #pmeter_p {
        background: #a6ff97;
        position: absolute;
        width: 0px;
        height: 15px;
        display: inline-block;
    }

    #pmeter_singlep {
        background: #a6ff97;
        position: absolute;
        width: 0px;
        height: 15px;
        display: inline-block;
    }

    a {
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    '''
    def wrap(pre, inner, post):
        return pre + inner + post

    def find_class(j, i):
        classes = []

        if data[j][i] == 0:
            classes.append('zero')

        if data[j][i] == 1:
            classes.append('one')

        return ' '.join(classes)

    frequencies = [sum(row) for j, row in enumerate(data)]

    data_rows = [
        ''.join(
            '<td id="' + str(i) +  ';' + str(j) + '" onclick="handle_click(this)" class="' + find_class(j, i) + '"></td>'
            for i, entry in enumerate(row)
        ) + '<td><span id="F' + str(j) + '">' + str(frequencies[j]) + '</span></td>'
        for j, row in enumerate(data)
    ]

    table = wrap(
        '<table class="heat">',
        '<th></th>'*(len(data[0])) + '<th>frequency</th>' + wrap(
            '<tr>',
            '</tr><tr>'.join(data_rows),
            '</tr>',
        ),
        '</table>',
    )
    table = wrap('<div class="tableheatbounder">', table, '</div>')
    title = '<p class="tabletitle"><span id="numfeatures">%s</span> features coinciding along <span class="numintersections" onmouseenter="highlight_intersections()" onmouseleave="unhighlight_intersections()">%s</span> samples</p>' % (len(data), len(intersections))

    single_p = calculate_probability_of_multicoincidence(len(data[0]), frequencies, len(intersections))
    p = coincidencetest(len(intersections), frequencies, len(data[0]))

    single_p = str(single_p)[0:9]
    p = str(p)[0:9]

    caption = '<p id="captiontext"><br>The probabilities are defined with respect to all configurations of 4 binary features with the given frequencies (<span id="frequencies">' + ', '.join(str(f) for f in frequencies)+ '</span>).<br></p>'
    tablestats = '<div class="tablestatsbounder"><table class="stats"><tr><td>Probability of exactly <span onmouseenter="highlight_intersections()" onmouseleave="unhighlight_intersections()" class="numintersections">' + str(len(intersections)) + '</span> coincidents</td><td class="pmeter"><span class="pmetercontainer"><span id="pmeter_singlep"></span></span></td><td class="pvals"><span id="singlep">' + str(single_p) + '</span></td></tr><td>Probability of <span class="numintersections" onmouseenter="highlight_intersections()" onmouseleave="unhighlight_intersections()">' + str(len(intersections)) + '</span> or more coincidents</td><td class="pmeter"><span class="pmetercontainer"><span id="pmeter_p"></span></span></td><td class="pvals"><span id="pvalue">' + str(p) + '</span></td><tr></tr></table></div>'

    html = '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><style>' + style + '</style><script>{{coincidencetest.js}}</script><script>{{fig_script.js}}</script></head><body onload="fill_fields(retrieve_data())">' + '<div class="figdiv">' + table + '<br><br>' + tablestats + title + caption  + '</div><p class="downloadpagecontainer"><a id="download_this_page" onmouseenter="update_download_link()" href="" title="figure.html" download="figure.html"><br>Download HTML</a></p></body></html>'
    return html

html = create_html(data)

coincidencetest_js = open('../webapp/coincidencetest.js', 'rt').read()
html = html.replace('{{coincidencetest.js}}', coincidencetest_js)

fig_script_js = open('fig_script.js', 'rt').read()
html = html.replace('{{fig_script.js}}', fig_script_js)

open('interactive_demo.html', 'wt').write(html)

