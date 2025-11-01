class JermaineSuperActionAI:
    def __init__(self, cycle: str, custodian: str):
        self.cycle = cycle
        self.custodian = custodian
        self.agents = {}

    def register_agent(self, name: str, agent):
        self.agents[name] = agent

    def invoke(self, name: str, **kwargs):
        if name not in self.agents:
            raise ValueError(f"No agent named {name}")
        result = self.agents[name].run(**kwargs)
        self.log_action(name, result)
        return result

    def log_action(self, agent_name: str, result: dict):
        print(f"[SuperAI] {agent_name} invoked under {self.cycle} "
              f"by {self.custodian}  {result}")
