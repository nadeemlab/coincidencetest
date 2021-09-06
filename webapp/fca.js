
function arrays_equal(a, b) {
    if (a.length !== b.length) return false;
    for (var i = 0; i < a.length; ++i) {
        if (a[i] !== b[i]) {
            return false;
        }
    }
    return true;
}

function compute_closure(set, data) {
    let N = set.length
    let samples = []
    for (let i = 0; i < data["samples"].length; i++) {
        accumulator = 0
        for (let j = 0; j < set.length; j++) {
            accumulator += data["samples"][i][set[j]]
        }
        if (accumulator == N) {
            samples.push(i)
        }
    }
    samples.sort()

    let M = samples.length
    let features = []
    for (let i = 0; i < data["features"].length; i++) {
        accumulator = 0
        for (let j = 0; j < samples.length; j++) {
            accumulator += data["features"][i][samples[j]]
        }
        if (accumulator == M) {
            features.push(i)
        }
    }
    features.sort()

    return {"closed set" : features, "dual set" : samples}
}

function already_have(set, sets) {
    for (I in sets) {
        other = sets[I]
        if (arrays_equal(set, other)) {
            return true
        }
    }
    return false
}

function get_all_pairs(list) {
    let results = []
    for (let i = 0; i < list.length - 1; i++) {
        for (let j = i + 1; j < list.length; j++) {
            results.push([list[i], list[j]])
        }
    }
    return results
}

function get_random_integer(min, max) {
  return Math.floor(Math.random() * (max - min + 1) ) + min;
}

function get_random_sample(list, size) {
    let sampled = []
    while (sampled.length < size) {
        sample = getRandomInteger(0, list.length - 1)
        if (sampled.includes(sample)) {
            continue
        } else {
            sampled.push(sample)
        }
    }
    return Array.from(sampled, (i) => list[i]).sort();
}

function do_pairwise_closures(closed_sets, dual_sets, computed_pairs, level_limit, data) {
    let range = Array(closed_sets.length).fill().map((x,i)=>i)
    let all_pairs = get_all_pairs(range)
    
    let a = new Set(all_pairs)
    let b = new Set(computed_pairs)
    let index_range = new Set([...a].filter(x => !b.has(x)));

    if (index_range.length == 0) {
        return
    }

    if ( !(level_limit == null) ) {
        new_pairs = get_random_sample(index_range, level_limit)
    }
    else {
        new_pairs = [...index_range]
    }

    for (I in new_pairs) {
        pair = new_pairs[I]

        index1 = pair[0]
        index2 = pair[1]

        a = new Set(closed_sets[index1]);
        b = new Set(closed_sets[index2]);
        union = new Set([...a, ...b]);
        union = [...union].sort()
        c = compute_closure(union, data)

        if ( !(c["dual set"].length == 0) ) {
            if ( !(already_have(c["closed set"], closed_sets)) ) {
                closed_sets.push(c["closed set"])
                dual_sets.push(c["dual set"])
            }
        }
        computed_pairs.push([index1, index2])
    }
}

function find_concepts(data, level_limit, max_recursion) {
    closed_sets = []
    dual_sets = []

    columns = Array(data['features'].length).fill().map((x,i)=>i)
    for (I in columns) {
        feature = columns[I]
        c = compute_closure([feature], data)
        if ( !(already_have(c["closed set"], closed_sets)) && !(c["dual set"].length == 0) ) {
            closed_sets.push(c["closed set"])
            dual_sets.push(c["dual set"])
        }
    }

    computed_pairs = []
    level = 1
    while (true) {
        previous_number_sets = closed_sets.length
        new_pairs_computed = do_pairwise_closures(closed_sets, dual_sets, computed_pairs, level_limit, data)
        new_number_sets = closed_sets.length
        if ( previous_number_sets == new_number_sets ) {
            break
        }
        if ( !(max_recursion == null) ) {
            if(level == max_recursion) {
                break
            }
        }
        level += 1
    }

    function get_named(indices, names) {
        named = []
        for (let k = 0; k < indices.length; k++) {
            named.push(names[indices[k]])
        }
        return named
    }

    named_signatures = Array.from(closed_sets, (s) => get_named(s, data["header"]))

    return [named_signatures, dual_sets]
}

