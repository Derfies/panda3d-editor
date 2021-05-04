from pandaEditor.nodes.tests.testmixin import TestMixin


class TestBaseMixin(TestMixin):

    component = None
    create_kwargs = {}

    def test_create(self):

        # TODO: Put this in a utility method, not an actual test.
        comp = self.component.create(**self.create_kwargs)
        comp.parent = comp.default_parent
        comp.set_default_values()
        self.assertTrue(isinstance(comp, self.component))
        return comp
