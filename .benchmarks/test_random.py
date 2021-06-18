import random


def test_generate_random_int_without_loop_with_list(benchmark):
    def func():
        rand = str(random.randint(0, 999999999999))
        result = ''.join(['0' for _ in range(12 - len(rand))]) + rand
        assert len(result) == 12
        return result

    benchmark(func)


def test_generate_random_int_without_loop_with_string_add(benchmark):
    def func():
        rand = str(random.randint(0, 999999999999))
        result = '0' * (12 - len(rand)) + rand
        assert len(result) == 12
        return result

    benchmark(func)


def test_generate_random_int_with_range(benchmark):
    def func():
        random_str = []
        for i in range(12):
            random_str.append(str(random.randint(0, 9)))
        result = ''.join(random_str)
        assert len(result) == 12
        return result
    benchmark(func)
