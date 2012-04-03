from behaviour import Behaviour
from attributes import FloatProperty, ComponentProperty

class TestBehaviour(Behaviour):

    velocity = FloatProperty(minimum=0.0, maximum=1.0)
    target = Component()

    def update(self):
        print self.velocity  # 0.0
        self.velocity = 1.0
        print self.velocity  # 1.0
        self.velocity = 2.0  # "assertion fail"
        print self.velocity  # 1.0
        print self.target    # None
        self.target = 1.232  # "assertion fail"
