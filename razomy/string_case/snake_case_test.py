from razomy.string_case import snake_case

def test_snake_case_converts_camel_case():
    assert snake_case('camelCase') == 'camel_case'

def test_snake_case_converts_pascal_case():
    assert snake_case('PascalCase') == 'pascal_case'

def test_snake_case_converts_kebab_case():
    assert snake_case('kebab-case') == 'kebab_case'

def test_snake_case_keeps_snake_case():
    assert snake_case('snake_case') == 'snake_case'

def test_snake_case_converts_sentence_casing():
    assert snake_case('Foo Bar') == 'foo_bar'

def test_snake_case_handles_mixed_delimiters():
    assert snake_case('foo.bar|baz') == 'foo_bar_baz'

def test_snake_case_trims_leading_trailing_delimiters():
    assert snake_case('__foo_bar__') == 'foo_bar'
    assert snake_case('-foo-bar-') == 'foo_bar'

def test_snake_case_handles_hyphen_plus_caps():
    assert snake_case('a-AA') == 'a_aa'

def test_snake_case_handles_acronyms_at_start():
    assert snake_case('JSONData') == 'json_data'

def test_snake_case_handles_acronyms_in_middle():
    assert snake_case('serverHTTPResponse') == 'server_http_response'

def test_snake_case_handles_acronyms_at_end():
    assert snake_case('parseXML') == 'parse_xml'

def test_snake_case_separates_numbers_adjacent_to_letters_1():
    assert snake_case('version2beta') == 'version_2_beta'
    assert snake_case('h2o') == 'h_2_o'

def test_snake_case_handles_numbers_correctly_in_kebab_snake_case():
    assert snake_case('version-10-beta') == 'version_10_beta'

def test_snake_case_returns_empty_string_for_empty_input():
    assert snake_case('') == ''

def test_snake_case_handles_single_characters():
    assert snake_case('A') == 'a'

def test_snake_case_preserves_special_characters_non_destructive_1():
    assert snake_case('C#Project') == 'c#project'
    assert snake_case('user@email.com') == 'user@email_com'
    assert snake_case('$$money$$') == '$$money$$'

def test_snake_case_splits_numbers_adjacent_to_letters_2():
    assert snake_case('version2beta') == 'version_2_beta'
    assert snake_case('foo123bar') == 'foo_123_bar'
    assert snake_case('404error') == '404_error'

def test_snake_case_handles_standard_camel_and_pascal_case_2():
    assert snake_case('camelCase') == 'camel_case'
    assert snake_case('PascalCase') == 'pascal_case'

def test_snake_case_handles_acronyms_intelligently_2():
    assert snake_case('JSONData') == 'json_data'
    assert snake_case('XMLHttpRequest') == 'xml_http_request'

def test_snake_case_collapses_mixed_delimiters_2():
    assert snake_case('foo  bar') == 'foo_bar'
    assert snake_case('foo-bar.baz') == 'foo_bar_baz'
    assert snake_case('a-AA') == 'a_aa'

def test_snake_case_returns_empty_string_for_empty_input_2():
    assert snake_case('') == ''