{{coincidencetest.js}}

{{fca.js}}


var tsv_object = {
    data : null,
}

var signatures_object = {
    closed_sets : [],
    dual_sets : [],
    p_values : [],
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

function do_one_coincidence_test() {
    let number_samples = tsv_object.data["samples"].length
    let number_features = tsv_object.data["features"].length
    i = signatures_object.closed_sets.length - 1
    let incidence_statistic = dual_sets[i].length
    let frequencies = get_frequencies(closed_sets[i])
    console.log(incidence_statistic + ", " + frequencies + ", " + number_samples)
    let p = coincidencetest(incidence_statistic, frequencies, number_samples, number_features)
    console.log("pvalue: " + p)
    signatures_object.p_values.push(p)
}

function pipeline(raw_data) {
    parsed = parse_table(raw_data)
    tsv_object.data = {
        "header" : parsed[0],
        "samples" : parsed.slice(1),
        "features" : nested_list_transpose(parsed.slice(1)),
    }
    signatures_object.total_samples = tsv_object.data["samples"].length

    single_addition_callback = function(c) {
        signatures_object.closed_sets.push(get_named(c["closed set"], tsv_object.data["header"]))
        signatures_object.dual_sets.push(c["dual set"])
        do_one_coincidence_test()
        // show_signatures()
        postMessage(signatures_object)
    }

    c = find_concepts(tsv_object.data, null, null, single_addition_callback)
    postMessage('Done with concepts.')
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

function worker_onmessage(event) {
    tsv_object = {
        data : null,
    }

    signatures_object = {
        closed_sets : [],
        dual_sets : [],
        p_values : [],
    }

    pipeline(event.data)
}

onmessage = worker_onmessage
