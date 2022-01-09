class Troll:

    _state = None

    life = 10
    hungry = 10
    safe = True

    def __init__(self, state: State) -> None:
        self.change_state(state)

    def change_state(self, state: State):
        self._state = state
        self._state.context = self

    def request1(self):
        self._state.handle1()

    def request2(self):
        self._state.handle2()

    def increase_life():
        self.life += 1

    def decrease_life():
        self.life -= 1

    def increase_hungry():
        self.hungry += 1

    def decrease_hungry():
        self.hungry -= 1


class State(ABC):
    @property
    def context(self) -> Troll:
        return self._context

    @context.setter
    def context(self, context: Troll) -> None:
        self._context = context

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def toggle_state(self) -> None:
        pass


class StateSleep(State):
    def execute(self) -> None:
        self.context.increase_life()
        self.context.decrease_hungry()
        print("StateSleep executed: hungry "+hungry+" | life: "+life)

    def toggle_state(self) -> None:
        if hungry < 5:
            self.context.change_state(StateBattle())
        elif safe == True :
            pass
        else:
            self.context.change_state(StateBattle())

class StateHunting(State):
    def execute(self) -> None:
        self.context.decrease_life()
        self.context.increase_hungry()
        print("StateHunting executed: hungry "+hungry+" | life: "+life)

    def toggle_state(self) -> None:
        self.context.change_state(StateSleep())

class StateBattle(State):
    def execute(self) -> None:
        self.context.decrease_life()
        print("StateBattle executed: hungry "+hungry+" | life: "+life)

    def toggle_state(self) -> None:
        self.context.change_state(StateSleep())
