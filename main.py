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

# # direction = 1 (up) | 2 (right) | 3 (down) | 4 (left)
# UP = 1
# RIGHT = 2
# DOWN = 3
# LEFT = 4

# estado = State()

# while True:
#     estado.reset(seed='', player_controlled=True, time_limit=1000)

#     # print(estado.world)

#     # estado.agent.inventory = [Ammo(), Medkit(), Food(), Water(), BaseballBat(), Knife(), Pistol(), Smg()]

#     estado.environment_start()
#     input("\n################################  Environment ended. Press Enter to reset the environment and start again...  ################################")
#     # estado.environment_start()
    




from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
import gymnasium as gym

import time
import os
from dotenv import load_dotenv, set_key
from pathlib import Path

from state import State

def render_env(env, model, sleep_time=1.0, result_time = 1.0):
    obs, info = env.reset()
    estado = State()
    total_achievement_count = 0
    total_reward_count = 0
    for _ in range(20):
        reward_count = 0
        while(True):
            action, _states = model.predict(obs, deterministic=False)
            obs, reward, terminated, truncated, info = env.step(action)
            env.render()
            reward_count += reward
            print(f"Reward: {reward} (invalid reward: {estado.invalid_return_value})")
            print(f"Action taken: {action}")
            time.sleep(sleep_time)  # Adjust the sleep time as needed for better visualization
            if truncated:
                obs, info = env.reset()
            if terminated:
                total = 0
                for key, information in info.items():
                    print(f"{key}: {information}")
                    total += information
                print(f"Total: {total}")
                total_achievement_count += total
                print(f"Reward total: {reward_count}")
                total_reward_count += reward_count
                time.sleep(result_time)
                obs, info = env.reset()
                break
    print(f"Total achievement count: {total_achievement_count}")
    print(f"Total reward count: {total_reward_count}")
    return total_achievement_count, total_reward_count
            
def reset_ppo_count(env_file_path):
    set_key(
        dotenv_path=env_file_path,
        key_to_set="PPO_COUNT",
        value_to_set='0'
    )
    print("PPO_COUNT reset to 0 in .env file.")
    env = gym.make("zombie-survival-v0")
    reset_model = PPO("MultiInputPolicy", env, verbose=1)
    reset_model.save("models/zombie_survival_ppo0")
    print("Initial PPO model saved with count: 0")
    exit(0)  # Exit after resetting PPO_COUNT and saving the initial model

gym.register(
    id='zombie-survival-v0',
    entry_point='gymAdaptation.placeholder:Placeholder',
    max_episode_steps=300,  # Prevent infinite episodes
)

env_file_path = Path("training.env")

load_dotenv(dotenv_path=env_file_path)
ppo_count = os.getenv("PPO_COUNT")
if ppo_count is None:
    ppo_count = 0
else:

    ppo_count = int(ppo_count)
print(f"PPO_COUNT from .env: {ppo_count}")

# reset_ppo_count(env_file_path)  # Reset PPO_COUNT to 0 and save the initial model before starting training

env = gym.make("zombie-survival-v0")
check_env(env)

# model = PPO.load(f"models/zombie_survival_ppo{(ppo_count-1)%4}")

model = PPO.load(f"models/zombie_survival_ppo15%")
render_env(env, model, sleep_time=0.0, result_time=0.0)
exit(0)

while(True):
    print(f"Starting PPO training with count: {ppo_count}")
    model = PPO.load(f"models/zombie_survival_ppo{ppo_count%4}", env=env)
    model.learn(total_timesteps=50000, log_interval=5) #roughly 6 minutes of training per iteration
    ppo_count += 1
    set_key(
        dotenv_path=env_file_path,
        key_to_set="PPO_COUNT",
        value_to_set=f"{ppo_count}"
    )
    model.save(f"models/zombie_survival_ppo{ppo_count%4}")
    if (ppo_count + 1) % 5 == 0:
        model.save(f"models/zombie_survival_ppo{ppo_count + 1}%")
    print(f"Saved PPO model with count: {ppo_count%4}")