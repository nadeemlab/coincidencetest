function falling_factorial(first, last) {
    let big_first = BigInt(first)
    let big_last = BigInt(last)
    let accumulator = BigInt(1)
    for (let k = last; k <= first; k++) {
        accumulator = accumulator * BigInt(k)
    }
    return accumulator
}

function factorial(number) {
    return falling_factorial(number, 1)
}

function binom(ambient_size, subset_size) {
    smaller = Math.min(subset_size, ambient_size - subset_size)
    larger = Math.max(subset_size, ambient_size - subset_size)
    return falling_factorial(ambient_size, larger + 1) / factorial(smaller)
}

function sign(x) {
    if (x % 2 == 0) {
        return 1
    } else {
        return -1
    }
}

function compute_number_of_covers(set_sizes, ambient_size) {
    let N = ambient_size
    let n = set_sizes
    accumulator = BigInt(0)
    for (let m = Math.max(...n); m < N+1; m++) {
        product = BigInt(1)
        for (let i = 0; i < n.length; i++) {
            product *= binom(m, n[i])
        }
        accumulator += BigInt(sign(N+m)) * binom(N,m) * product
    }
    return accumulator
}

function count_all_configurations(set_sizes, ambient_size) {
    product = BigInt(1)
    for (let i = 0; i < set_sizes.length; i++) {
        product *= binom(ambient_size, set_sizes[i])
    }
    return product
}

function calculate_probability_of_multicoincidence(ambient_size, set_sizes, intersection_size) {
    reduced_sizes = []
    for (let i = 0; i < set_sizes.length; i++) {
        reduced_sizes.push(set_sizes[i] - intersection_size)
    }

    initial_choices = binom(ambient_size, intersection_size)
    reduced_ambient_size = ambient_size - intersection_size
    complementary_sizes = []
    for (let i = 0; i < reduced_sizes.length; i++) {
        complementary_sizes.push(reduced_ambient_size - reduced_sizes[i])
    }
    covers_of_remaining = compute_number_of_covers(complementary_sizes, reduced_ambient_size)
    all_configurations = count_all_configurations(set_sizes, ambient_size)
    precision = 10000000000000000
    return (Number(initial_choices * covers_of_remaining * BigInt(precision) / all_configurations) / precision)
}

function coincidencetest(incidence_statistic, frequencies, number_samples, correction_feature_set_size) {
    accumulator = 0
    for (let I = incidence_statistic; I <= Math.min(...frequencies); I++) {
        accumulator += calculate_probability_of_multicoincidence(number_samples, frequencies, I)
        if (accumulator > 0.9) {
            accumulator = 1.0
            break
        }
    }
    if ( !(correction_feature_set_size == null) ) {
        accumulator = accumulator * parseInt(binom(correction_feature_set_size, frequencies.length))
        if (accumulator > 1.0) {
            accumulator = 1.0
        }
    }
    return accumulator
}
