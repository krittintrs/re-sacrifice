class StateMachine:
    def __init__(self):
        self.current = None

    def SetScreen(self, screen):
        self.screen = screen

    def SetStates(self, states):
        self.states = states

    def Change(self, state_name, enter_params=None):
        assert(self.states[state_name]) #
        if self.current:
            self.current.Exit()
        self.current = self.states[state_name]
        self.current.Enter(enter_params)

        self.state_name = state_name

    def update(self, dt, events):
        self.current.update(dt, events)

    def render(self):
        self.current.render(self.screen)

    # for entity
    def ProcessAI(self, params, dt):
        self.current.ProcessAI(params, dt)