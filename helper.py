import pprint


def generate_killer_combinations():
    result = {
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {},
        7: {},
        8: {},
        9: {}
    }
    for length in range(1, 10):
        for total in range((length ** 2 + length) // 2, int(-(length ** 2) / 2 + 9.5 * length + 1)):
            curr = [set()]
            for i in range(length):
                temp = []
                for current_option in curr:
                    for add_attempt in range(1, 10):
                        if sum(current_option) + add_attempt <= total and not(add_attempt in current_option):
                            if not(current_option.union({add_attempt}) in temp):
                                temp.append(current_option.union({add_attempt}))
                curr = temp

            result[length][total] = list(filter(lambda val: sum(val) == total, curr))

    # pprint.pprint(result)

    return result
