from ld1py.meta import SingletonMeta


def test_singleton_class_is_created_only_once(mocker):
    class SingletonClass(metaclass=SingletonMeta):
        def __init__(self, stub):
            super().__init__()
            stub("called")

    stub = mocker.stub(name="on_init_stub")

    first = SingletonClass(stub)
    second = SingletonClass(stub)

    assert first is second
    stub.assert_called_once()


def test_reset_removes_registered_singleton_instances():
    class SingletonClass(metaclass=SingletonMeta):
        pass

    first = SingletonClass()
    second = SingletonClass()

    assert first is second

    SingletonMeta.reset()

    third = SingletonClass()

    assert first is not third


def test_cleanup_cleans_up_all_instances(mocker):
    class SingletonClass(metaclass=SingletonMeta):
        def _cleanup(self):
            pass

    obj = SingletonClass()
    spied = mocker.spy(obj, "_cleanup")

    SingletonMeta.cleanup()
    spied.assert_called_once()
