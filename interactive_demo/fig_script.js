
data_obj = {
    data : [
        [1,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,1,1,1],
        [0,0,1,0,1,1,0,0,1,1,0,1,1,0,0,1,0,1,1,1],
        [0,0,1,1,0,0,0,0,0,1,0,1,0,1,0,1,1,1,1,1],
        [0,1,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0,1,1,1],
    ]
}

function retrieve_data() {
    for (let j = 0; j < data_obj.data.length; j++) {
        for (let i =0; i < data_obj.data[0].length; i++) {
            let element = document.getElementById(i + ';' + j)
            if (element.classList.contains('one')) {
                data_obj.data[j][i] = 1
            } else {
                data_obj.data[j][i] = 0
            }
        }
    }
    return data_obj.data
}

function sum(row) {
    let accumulator = 0
    for (let k = 0; k < row.length ; k++) {
        accumulator += row[k]
    }
    return accumulator
}

function get_frequency(j) {
    return sum(data_obj.data[j])
}

function get_frequencies(data) {
    let frequencies = []
    for (let k = 0; k < data.length ; k++) {
        frequencies.push(sum(data[k]))
    }
    return frequencies
}

function get_intersections(data) {
    let included = 0
    for (let i = 0; i < data[0].length; i++) {
        let number_in = 0
        for (let j = 0; j < data.length; j++) {
            if (data[j][i] == 1) {
                number_in += 1
            }
        }
        if (number_in == data_obj.data.length) {
            included += 1
        }
    }
    return included
}

function fill_fields(data) {
    let frequencies = get_frequencies(data)
    let number_intersections = get_intersections(data)

    document.getElementById("numfeatures").innerText = data.length + ""
    document.getElementById("frequencies").innerText = frequencies.join(', ')

    let inter = document.getElementsByClassName("numintersections")
    for (let k = 0; k < inter.length; k++) {
        inter[k].innerText = "" + number_intersections
    }

    for (let j = 0; j < data.length; j++) {
        document.getElementById("F" + j).innerText = get_frequency(j)
    }

    let ambient_size = data[0].length
    let intersection_size = number_intersections
    let set_sizes = frequencies
    let singlep = calculate_probability_of_multicoincidence(ambient_size, set_sizes, intersection_size)
    let pvalue = coincidencetest(intersection_size, set_sizes, ambient_size, null)

    document.getElementById("singlep").innerText = singlep
    document.getElementById("pvalue").innerText = pvalue

    draw_p_meters()

    // update_download_link()
}

function handle_click(element) {
    element.classList.toggle('zero');
    element.classList.toggle('one');
    fill_fields(retrieve_data())
}

function change_highlight_intersections(flag) {
    let data = data_obj.data
    for (let i = 0; i < data[0].length; i++) {
        let number_in = 0
        for (let j = 0; j < data.length; j++) {
            if (data[j][i] == 1) {
                number_in += 1
            }
        }
        if (number_in == data_obj.data.length) {
            for (let j = 0; j < data.length; j++) {
                let element = document.getElementById(i + ';' + j)
                if (flag) {
                    element.classList.add('highlight')
                } else {                    
                    element.classList.remove('highlight')
                }
            }
        }
    }
}

function highlight_intersections() {
    change_highlight_intersections(true)
}

function unhighlight_intersections() {
    change_highlight_intersections(false)    
}

function draw_p_meter(element_name, value) {
    var c = document.getElementById(element_name);
    c.style.width = parseInt(180 * value) + 'px'
    console.log('Element "' + element_name + '"...')
    console.log('New c.style.width: ' + parseInt(180 * value))
    // var ctx = c.getContext("2d");
    // ctx.beginPath()
    // ctx.clearRect(0, 0, c.width, c.height);
    // ctx.lineWidth = "1"
    // ctx.strokeStyle = "#999999"
    // ctx.fillStyle = "#a6ff97"
    // // ctx.fillRect(1, 1, c.width-1, c.height-1);
    // ctx.fillRect(0,0, parseInt(c.width * value), c.height)
    // ctx.rect(-1,0, parseInt(c.width * value), c.height)
    // ctx.stroke();
}

function draw_p_meters() {
    singlep = parseFloat(document.getElementById("singlep").innerText)
    pvalue = parseFloat(document.getElementById("pvalue").innerText)
    draw_p_meter("pmeter_singlep", singlep)
    draw_p_meter("pmeter_p", pvalue)
}

function update_download_link() {
    var s = new XMLSerializer();  //Copy document to new object then remove the download link anchor?
    var str = s.serializeToString(document);
    base64str = btoa(str)
    download_link = document.getElementById('download_this_page')
    download_link.href = 'data: text/html;base64,' + base64str
    console.log(base64str)
    return true
}
