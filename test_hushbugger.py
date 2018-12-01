import sys

from hushbugger import Dummy, hush

PY3 = sys.version_info >= (3,)


def test_ordinary_return():
    @hush
    def func():
        return 100

    assert func() == 100


if PY3:

    def test_const_return():
        @hush
        def func():
            raise Exception
            return 15

        assert func() == 15

        @hush
        def func():
            [].pop()
            return 3 * 5

        assert func() == 15

    def test_local_return():
        @hush
        def func(x):
            "foo" / "bar"
            return x

        obj = object()
        assert func(obj) is obj

    some_global = object()

    def test_global_return():
        @hush
        def func():
            str.join(1, 2)
            return some_global

        assert func() is some_global

    def test_nonlocal_return():
        some_nonlocal = object()

        @hush
        def func():
            (lambda x: x(x))(lambda x: x(x))
            return some_nonlocal

        assert func() is some_nonlocal


else:

    def test_py2_dummy():
        @hush
        def func():
            0 / 0
            return {}

        assert isinstance(func(), Dummy)


def test_dummy_fallback():
    @hush
    def func():
        1 .foo
        return []

    assert isinstance(func(), Dummy)


def test_dummy_resilience():
    d = Dummy()
    d + 10
    10 + d
    list(d)
    bool(d)
    str(d)
    d.d.d.d.d.d()()()[0](foo=20)[1:2:3].bar.baz
    ~d
    -d
    +d
    not d
    abs(d)
    int(d)
    float(d)
    complex(d)
    if not PY3:
        long(d)
    dict(d)  # I don't understand why this works, let me know if you figure it out
    del d.foo
    del d[3]
    d[3] = 100
    d.x = 100
    d | 3 | 3 | 3 | 3 | 3
    d in d
    () in d
    [e for e in d if e is d]


def test_dummy_repr():
    assert "Coalescer" in repr(Dummy())
    assert "foo.Coalescer" in repr(Dummy("foo"))


def test_almost_realistic_scenario():
    @hush
    def sum_list(nums):
        total = 0
        index = 0
        while index <= len(nums):
            # Fails when index == len(nums)
            total += nums[index]
            index += 1
        return total

    assert sum_list([1, 2, 3]) == 6
    assert sum_list([1, 2, "3"]) == 3
