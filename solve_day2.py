from typing import Generator

example = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

puzzle = "2157315-2351307,9277418835-9277548385,4316210399-4316270469,5108-10166,872858020-872881548,537939-575851,712-1001,326613-416466,53866-90153,907856-1011878,145-267,806649-874324,6161532344-6161720341,1-19,543444404-543597493,35316486-35418695,20-38,84775309-84908167,197736-309460,112892-187377,336-552,4789179-4964962,726183-793532,595834-656619,1838-3473,3529-5102,48-84,92914229-92940627,65847714-65945664,64090783-64286175,419838-474093,85-113,34939-52753,14849-30381"

def invalid_product_id(product_id: str) -> bool:
    if len(product_id) % 2 == 1:
        return False
    first_half = product_id[:len(product_id) // 2]
    second_half = product_id[len(product_id) // 2:]
    return first_half == second_half

def invalid_product_id_generator(
        product_id: str,
    ) -> Generator[str, None, None]:
    if len(product_id) % 2 == 1:
        for pid in invalid_product_id_generator("1" + "0" * len(product_id)):
            yield pid
    else:
        first_half = int(product_id[:len(product_id) // 2])
        second_half = int(product_id[len(product_id) // 2:])
        if first_half == second_half:
            v = int(product_id)
        elif first_half > second_half:
            v = int(f"{first_half}{first_half}")
        else:
            v = int(f"{first_half+1}{first_half+1}")

        yield str(v)

        for pid in invalid_product_id_generator(str(v + 1)):
            yield pid

def test_invalid_product_id_generator():
    a = 444545
    b = 884568
    
    expected = set()
    for x in range(a, b+1):
        if invalid_product_id(str(x)):
            expected.add(x)

    found = set()
    for x in invalid_product_id_generator(str(a)):
        if int(x) > b:
            break
        assert invalid_product_id(str(x))
        found.add(int(x))
    assert expected.difference(found) == set()
    assert found.difference(expected) == set()

def solve_1(data: str):
    product_ranges = data.split(",")
    product_ids = [tuple(pr.split("-")) for pr in product_ranges]
    total = 0
    for pr1, pr2 in product_ids:
        # print(f"range: {pr1} {pr2}")
        for pr in invalid_product_id_generator(pr1):
            if int(pr) > int(pr2):
                break
            # print(f"\t {pr} should be invalid")
            if invalid_product_id(str(pr)):
                total += int(pr)

    return total


def invalid_product_id_generator2(
        product_id: str,
        max_id: str,
    ) -> Generator[str, None, None]:
    
    for digits in range(len(product_id), len(max_id) + 1):
        # print(f"{digits=}")
        for pattern_size in range(1, digits):
            repeat, remainder = divmod(digits, pattern_size)
            if remainder != 0:
                continue
            for number in range(1, 10**pattern_size):
                invalid_product_id_str = str(number) * repeat
                # print(f"{invalid_product_id_str=}")
                yield invalid_product_id_str


def solve_2(data: str):
    product_ranges = data.split(",")
    product_ids = [tuple(pr.split("-")) for pr in product_ranges]
    total = 0
    for pr1, pr2 in product_ids:
        # print(f"range: {pr1} {pr2}")
        uniques = set()
        for x in invalid_product_id_generator2(pr1, pr2):
            if int(pr1) <= int(x) <= int(pr2):
                uniques.add(int(x))
        # print(f"\t{uniques=}")
        for x in uniques:
            total += x
    return total


if __name__ == "__main__":
    print(solve_1(example))
    print(solve_1(puzzle))
    print(solve_2(example))
    print(solve_2(puzzle))
