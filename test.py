import gym
from environment import VacuumWorldEnv

gym.register(
    id='VacuumWorld-v0',
    entry_point='environment:VacuumWorldEnv',
    kwargs={'n_cols': 5, 'n_rows': 5, 'max_timestep': None}
)
env = gym.make('VacuumWorld-v0', n_cols=2, n_rows=1, max_timestep=10)
env.reset()

for i in range(100):
    print(f"--- Step: {i} ---")
    action = env.action_space.sample()
    print(env.step(action))
