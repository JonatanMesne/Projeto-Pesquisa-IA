# from items.item import Item
# from items.ammo import Ammo
# from items.medkit import Medkit
# from items.food import Food
# from items.water import Water
# from items.weapons.baseball_bat import BaseballBat
# from items.weapons.knife import Knife
# from items.weapons.pistol import Pistol
# from items.weapons.smg import Smg

# from state import State

#direction = 1 (up) | 2 (right) | 3 (down) | 4 (left)
# UP = 1
# RIGHT = 2
# DOWN = 3
# LEFT = 4

# estado = State()

# while True:
    # estado.reset(seed='', player_controlled=True, time_limit=1000)

    # print(estado.world)

    # estado.agent.inventory = [Ammo(), Medkit(), Food(), Water(), BaseballBat(), Knife(), Pistol(), Smg()]

    # estado.environment_start()
    




from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
import gymnasium as gym

import time

gym.register(
    id='zombie-survival-v0',
    entry_point='gymAdaptation.placeholder:Placeholder',
    # max_episode_steps=300,  # Prevent infinite episodes
)

env = gym.make("zombie-survival-v0")
check_env(env)

model = PPO("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=10000, log_interval=500)
model.save("zombie_survival_ppo")

del model # remove to demonstrate saving and loading

model = PPO.load("zombie_survival_ppo")

obs, info = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    print(f"Reward: {reward}")
    print(f"Action taken: {action}")
    time.sleep(1)  # Adjust the sleep time as needed for better visualization
    if terminated or truncated:
        obs, info = env.reset()