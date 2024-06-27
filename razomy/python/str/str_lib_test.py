from razomy.python.str import str_lib


def test_find_most_similar_key():
    # Sample object
    obj = {'key1': 'value1', 'key3': 'value3', 'key4': 'value4'}
    key_to_match = 'key4_42'
    # Finding the most similar key
    most_similar_key = str_lib.find_most_similar_key(obj, key_to_match)
    print("Most similar key:", most_similar_key)
    assert most_similar_key == 'key4'


def test_short():
    print(str_lib.short('01234567899876543210'))
