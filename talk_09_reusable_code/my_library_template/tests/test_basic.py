import my_library as ml
from my_library.basic import helloworld


def test_module_docstring():

    assert "useful" in ml.__doc__


def test_helloworld():
    num = helloworld()
    assert num == 2