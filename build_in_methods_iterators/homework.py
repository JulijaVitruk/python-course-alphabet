from typing import List, Dict, Union, Generator
import random
import string



# we will work with such dicts
ST = Dict[str, Union[str, int]]
# and we will put this dicts in list
DT = List[ST]


def task_1_fix_names_start_letter(data: DT) -> DT:
    """
    make all `names` field in list of students to start from upper letter

    examples:
        fix_names_start_letters([{'name': 'alex', 'age': 26}, {'name': 'denys', 'age': 89}])
        >>> [{'name': 'alex', 'age': 26}, {'name': 'denys', 'age': 89}]
    """

    def func(x: dict):
        ret = None
        if x.get('name') is not None:
            ret = x.get('name')[0].upper()+x.get('name')[1:]
            x['name']=ret
        return ret

    for y in range(len(data)):
        func(data[y])

    return data


def task_2_remove_dict_fields(data: DT, redundant_keys: List[str]) -> DT:
    """given_data
    remove from dictionaries given key value

    examples:
       remove_dict_field([{'name': 'alex', 'age': 26}, {'name': 'denys', 'age': 89}], 'age')
        >>> [{'name': 'alex'}, {'name': 'denys'}]
    """
    data1 = []
    for a in range(len(data)):
        our_dict = data[a]
        for ke in redundant_keys:
            del our_dict[ke]
        data1.append(our_dict)

    return data1


def task_3_find_item_via_value(data: DT, value) -> DT:
    """
    find and return all items that has @searching value in any key
    examples:
        find_item_via_value([{'name': 'alex', 'age': 26}, {'name': 'denys', 'age': 89}], 26)
        >>> [{'name': 'alex', 'age': 26}]
    """
    return [x for x in data if value in x.values()]


def task_4_min_value_integers(data: List[int]) -> int:
    """
    find and return minimum value from list
    """
    if bool(data) is True:
        our_min = min(data)
    else:
        our_min = None

    return our_min




def task_5_min_value_strings(data: List[Union[str, int]]) -> str:
    """
    find the shortest string
    """
    result = None
    dict_of_len = {str(x): len(str(x)) for x in data}
    for x in dict_of_len:
        if dict_of_len[x] == min(dict_of_len.values()):
            result = x

    return result


def task_6_min_value_list_of_dicts(data: DT, key: str) -> ST:
    """
    find minimum value by given key()lambda
    returns:

    """

    data1 = filter(lambda item: item.get(key) is not None, data)
    return min(data1, key=lambda item: item.get(key))


def task_7_max_value_list_of_lists(data: List[List[int]]) -> int:
    """
    find max value from list of lists
    """
    return max(max(data))


def task_8_sum_of_ints(data: List[int]) -> int:
    """
    find sum of all items in given list
    """
    return sum(data)


def task_9_sum_characters_positions(text: str) -> int:
    """
    please read first about ascii table.
    https://python-reference.readthedocs.io/en/latest/docs/str/ascii.html
    you need to calculate sum of decimal value of each symbol in text
        examples:
        task_9_sum_characters_positions("a")
        >>> 65
        task_9_sum_characters_positions("hello")
        >>> 532

    """

    return sum([ord(text[i]) for i in range(len(text))])



def task_10_generator_of_simple_numbers() -> Generator[int, None, None]:
    """
    return generator of simple numbers
    stop then iteration if returned value is more than 200
    examples:
        a = task_10_generator_of_simple_numbers()
        next(a)
        >>> 2
        next(a)
        >>> 3
    """

    n = [2, 3]
    yield 2
    yield 3
    i = 3
    while i <= 210:
        ost = [i % n[j] for j in range(len(n))]
        if all(ost) is True:
            yield i
            n.append(i)
            i += 1
        else:
            i += 1





def task_11_create_list_of_random_characters() -> List[str]:
    """
    create list of 20 elements where each element is random letter from latin alphabet

    """
    list_of_rannum = [random.randint(0, len(string.ascii_lowercase)-1) for _ in range(20)]

    return [string.ascii_lowercase[list_of_rannum[x]] for x in range(20)]





