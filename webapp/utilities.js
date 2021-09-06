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

function openDialog() {
    document.getElementById('progressarea').hidden = false
    read_tsv(document.getElementById('uploadbutton'))
}

function read_tsv(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();
        reader.readAsBinaryString(input.files[0]);
        reader.onload = function (event) {
            spawn_worker(event)
        }
    }
}

function spawn_worker(event) {
    if (typeof(worker) == "undefined") {
        worker = new Worker("./worker.js");
        // worker = new Worker(URL.createObjectURL(new Blob([worker_function.toString()], {type: 'text/javascript'})));
        // worker = new Worker(URL.createObjectURL(new Blob([worker_function.toString()], {type: 'text/javascript'})));
        console.log('Spawned worker.')
        worker.onmessage = onmessage
        worker.postMessage(event.target.result)
    }
}

function onmessage(event) {
    console.log('Received message from worker.')

    if (event.data == "Done with concepts.") {
        document.getElementById('progressarea').hidden = true
    }
    else {
        signatures_object = event.data
        show_signatures(signatures_object)
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

function show_signatures(signatures_object) {
    o = signatures_object
    table_rows = []
    for (let i = 0; i < o.closed_sets.length; i++) {
        if (o.closed_sets[i].length == 1) {
            continue
        }
        table_rows.push([o.closed_sets[i].sort().join(' '), o.dual_sets[i].length, o.p_values[i]])
    }
    table_rows.sort(function(row1, row2) {return row1[2] - row2[2]})

    table_header = ["Signature", "Frequency<br>(out of " + signatures_object.total_samples + ")", "p-value"]

    p0 = '<table class="signaturestable"><tr>' + "<th>" + table_header.join("</th><th>") + "</th></tr>"
    p1 = ""
    for (let k = 0; k < table_rows.length; k++) {
        class_specifier = classify_p_value(table_rows[k][2])
        p1 += "<tr" + class_specifier + "><td>" + table_rows[k].join("</td><td>") + '</td></tr>\n'
    }
    p2 = "</table>"
    document.getElementById('resultsarea').innerHTML = p0 + p1 + p2
}
