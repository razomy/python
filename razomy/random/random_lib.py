import random
import typing


def random_choice_priority(*items: typing.Tuple[typing.Any, float]):
    total_priority = sum(i[1] for i in items)
    random_value = random.uniform(0, total_priority)

    for item, priority in items:
        random_value -= priority
        if random_value <= 0:
            return item


def test_random_choice_priority():
    print('a', random_choice_priority(('a', .9), ('b', .1)))
    print('a', random_choice_priority(('a', .9), ('b', .1)))
    print('a', random_choice_priority(('a', .9), ('b', .1)))
    print('a', random_choice_priority(('a', .9), ('b', .1)))

    print('b', random_choice_priority(('a', .1), ('b', .9)))
    print('b', random_choice_priority(('a', .1), ('b', .9)))
    print('b', random_choice_priority(('a', .1), ('b', .9)))
    print('b', random_choice_priority(('a', .1), ('b', .9)))

    print('b', random_choice_priority(('a', .1), ('b', .8), ('c', .1)))
    print('b', random_choice_priority(('a', .1), ('b', .8), ('c', .1)))
    print('b', random_choice_priority(('a', .1), ('b', .8), ('c', .1)))
    print('b', random_choice_priority(('a', .1), ('b', .8), ('c', .1)))

    print('ab', random_choice_priority(('a', .1), ('b', .1)))
    print('ab', random_choice_priority(('a', .1), ('b', .1)))
    print('ab', random_choice_priority(('a', .1), ('b', .1)))
    print('ab', random_choice_priority(('a', .1), ('b', .1)))

    print('abc', random_choice_priority(('a', .3), ('b', .3), ('c', .3)))
    print('abc', random_choice_priority(('a', .3), ('b', .3), ('c', .3)))
    print('abc', random_choice_priority(('a', .3), ('b', .3), ('c', .3)))
    print('abc', random_choice_priority(('a', .3), ('b', .3), ('c', .3)))
