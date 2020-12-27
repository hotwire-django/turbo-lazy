from turbo.lazy.templatetags.lazy import is_int


def test_is_int_with_int():
    assert is_int(123)
    assert is_int("123")


def test_is_int_with_string():
    assert not is_int("Hello")
