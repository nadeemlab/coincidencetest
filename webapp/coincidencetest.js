function setup(){
    document.getElementById('uploadbutton').addEventListener('change', openDialog);
}

function show_tooltip(element) {
    children = element.children
    last_child = children[children.length - 1]
    last_child.hidden = false
}

function unshow_tooltip(element) {
    children = element.children
    last_child = children[children.length - 1]
    last_child.hidden = true
}

var obj_csv = {
    size : 0,
    dataFile : [],
    data : null,
};

function openDialog() {
    document.getElementById('progressarea').hidden = false
    read_csv(document.getElementById('uploadbutton'))
}

function read_csv(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();
        reader.readAsBinaryString(input.files[0]);
        reader.onload = function (e) {
            obj_csv.size = e.total;
            obj_csv.dataFile = e.target.result
            parsed = parse_table(obj_csv.dataFile)
            // document.getElementById('area').innerHTML = create_html_table(parsed)
            data = {
                "header" : parsed[0],
                "samples" : parsed.slice(1),
                "features" : nested_list_transpose(parsed.slice(1)),
            }
            c = find_concepts(data, null, null)
            let closed_sets = c[0]
            let dual_sets = c[1]

            document.getElementById('progressarea').hidden = true

            table_rows = []
            for (let i = 0; i < closed_sets.length; i++) {
                if (closed_sets[i].length == 1) {
                    continue
                }
                table_rows.push([closed_sets[i].sort().join('; '), dual_sets[i].length, '...'])
            }
            table_header = ["Signature", "Frequency (out of " + data["samples"].length + ")", "p-value"]

            p0 = "<table><tr>" + "<th>" + table_header.join("</th><th>") + "</th></tr>"
            p1 = ""
            for (let k = 0; k < table_rows.length; k++) {
                p1 += "<tr><td>" + table_rows[k].join("</td><td>") + "</td></tr>\n"
            }
            p2 = "</table>"
            document.getElementById('resultsarea').innerHTML = p0 + p1 + p2

        }
    }
}

function nested_list_transpose(nested_list) {
    transposed = Array(nested_list[0].length).fill(null)
    for (let j = 0; j < transposed.length; j++) {
        transposed[j] = Array(nested_list.length).fill(0)
    }

    for (let i = 0; i < nested_list.length; i++) {
        for (let j = 0; j < nested_list[0].length; j++) {
            transposed[j][i] = nested_list[i][j]
        }
    }
    return transposed
}

function parse_table(text){
    let csv_data = []
    let lines = text.trim().split('\n')
    csv_data.push(lines[0].split('\t'))
    for (let i = 1; i < lines.length; i++) {
        let row = []
        splitted = lines[i].split('\t')
        for (let j = 0; j < splitted.length; j++) {
            if ( splitted[j] == '0' || splitted[j] == '1' ) {
                row.push(parseInt(splitted[j]))
            }
            else {
                row.push(splitted[j])
            }
        }
        csv_data.push(row)
    }
    return csv_data
}

function create_html_table(data) {
    txt = ""
    txt += "<table>"
    txt += "<tr>"
    for (let j = 0; j < data[0].length; j++) {
        txt += "<th>"
        txt += data[0][j]
        txt += "</th>"
    }
    txt += "</tr>"
    for (let i = 1; i < data.length; i++) {
        txt += "<tr>"
        for (let j=0; j< data[i].length; j++) {
            txt += "<td>"
            txt += data[i][j]
            txt += "</td>"
        }
        txt += "</tr>"
    }
    return ("Number of lines found: " + (data.length-1) + '\n' + txt)
}
