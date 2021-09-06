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

var tsv_object = {
    size : 0,
    data : null,
};

var signatures_object = {
    closed_sets : null,
    dual_sets : null,
    p_values : null,
    signatures : null,
}

function get_frequencies(feature_indices) {
    frequencies = []
    for (let k = 0; k < feature_indices.length; k++) {
        i = feature_indices[k]
        feature = tsv_object.data["features"][i]
        sum = feature.reduce((a, b) => a + b, 0)
        frequencies.push(sum)
    }
    return frequencies
}

function do_coincidence_tests() {
    let number_samples = tsv_object.data["samples"].length
    let number_features = tsv_object.data["features"].length
    signatures_object.p_values = []
    for (let i = 0; i < signatures_object.closed_sets.length; i++) {
        let incidence_statistic = dual_sets[i].length
        let frequencies = get_frequencies(closed_sets[i])
        console.log(incidence_statistic + ", " + frequencies + ", " + number_samples)
        let p = coincidencetest(incidence_statistic, frequencies, number_samples, number_features)
        console.log("pvalue: " + p)
        signatures_object.p_values.push(p)
    }
}

function classify_p_value(p) {
    if (p < 0.01) {
        return ' class="extreme"'
    }
    if (p < 0.05) {
        return ' class="significant"'
    }
    return ' class="insignificant"'
}

function show_signatures() {
    o = signatures_object
    table_rows = []
    for (let i = 0; i < o.closed_sets.length; i++) {
        if (o.closed_sets[i].length == 1) {
            continue
        }
        table_rows.push([o.closed_sets[i].sort().join(' '), o.dual_sets[i].length, o.p_values[i]])
    }
    console.log(table_rows)
    table_rows.sort(function(row1, row2) {return row1[2] - row2[2]})
    console.log("After sorting...")
    console.log(table_rows)

    table_header = ["Signature", "Frequency<br>(out of " + tsv_object.data["samples"].length + ")", "p-value"]

    p0 = '<table class="signaturestable"><tr>' + "<th>" + table_header.join("</th><th>") + "</th></tr>"
    p1 = ""
    for (let k = 0; k < table_rows.length; k++) {
        class_specifier = classify_p_value(table_rows[k][2])
        p1 += "<tr" + class_specifier + "><td>" + table_rows[k].join("</td><td>") + '</td></tr>\n'
    }
    p2 = "</table>"
    document.getElementById('resultsarea').innerHTML = p0 + p1 + p2
    signatures_object.signatures = table_rows
}

function openDialog() {
    document.getElementById('progressarea').hidden = false
    read_tsv(document.getElementById('uploadbutton'))
}

function pipeline(event) {
    tsv_object.size = event.total;
    parsed = parse_table(event.target.result)
    tsv_object.data = {
        "header" : parsed[0],
        "samples" : parsed.slice(1),
        "features" : nested_list_transpose(parsed.slice(1)),
    }
    c = find_concepts(tsv_object.data, null, null)
    signatures_object.closed_sets = c[0]
    signatures_object.dual_sets = c[1]

    do_coincidence_tests()
    show_signatures()

    document.getElementById('progressarea').hidden = true
}

function read_tsv(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();
        reader.readAsBinaryString(input.files[0]);
        reader.onload = function (event) {
            pipeline(event)
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
    let rows = []
    let lines = text.trim().split('\n')
    rows.push(lines[0].split('\t'))
    for (let i = 1; i < lines.length; i++) {
        let row = []
        splitted = lines[i].split('\t')
        for (let j = 0; j < splitted.length; j++) {
            if ( splitted[j] == '0' || splitted[j] == '1' ) {
                row.push(parseInt(splitted[j]))
            }
            else {
                console.warn("Table data should be binary, '1' or '0'.")
            }
        }
        rows.push(row)
    }
    return rows
}
