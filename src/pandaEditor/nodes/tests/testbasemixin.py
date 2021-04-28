from pandaEditor.nodes.tests.testmixin import TestMixin


class TestBaseMixin(TestMixin):

    component = None
    create_kwargs = {}

    def test_create(self):
        comp = self.component.create(**self.create_kwargs)
        comp.set_default_parent()
        comp.set_default_values()
        return comp
