import gym
from environment import VacuumWorldEnv
from agents import TraGent

gym.register(
    id='VacuumWorld-v0',
    entry_point='environment:VacuumWorldEnv',
    kwargs={'n_cols': 5, 'n_rows': 5, 'max_timestep': None}
)
env = gym.make('VacuumWorld-v0', n_cols=2, n_rows=2, max_timestep=30)
obs, info = env.reset()
tragent = TraGent()
for i in range(30):
    print(f"--- Step: {i} ---")
    print(obs)
    action = tragent.act(obs, False)
    print(f'action: {action}')
    print(f'memory_stack: {tragent.memory_stack}')
    print(f'destination: {tragent.destination}')
    print(f'prev_action:{tragent.prev_action}')
    print(tragent.stal_flag)
    obs, reward, term, info = env.step(action)
