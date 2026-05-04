from typing import Any, SupportsFloat

import gymnasium as gym
import numpy as np
from gymnasium import Space, spaces
from gymnasium.core import ObsType, ActType, RenderFrame

from actions.update_vision import UpdateVision
from entities.agent import Agent
from state import State

class Placeholder(gym.Env):
    # Inicializa um novo ambiente de simulação
    def __init__(self, seed=None, time_limit=1000, render_mode=None):
        self.render_mode = render_mode
        self.seed = seed
        self.time_limit = time_limit
        self.state = State()
        self.state.reset(seed=self.seed, player_controlled=False, time_limit=self.time_limit)
        
        #o gemini criticou o action space ser apenas discreto
        self.action_space = spaces.Discrete(28 + Agent.max_inventory_space * 2)   #28 standard actions + change held item for each inventory slot + drop item for each inventory slot
        
        # vision_data = []    #created separately because it can't be a ndarray, it needs to be a list of lists
        # for i in range(self.state.agent.vision_range*2+1):
        #     vision_data.append([])
        #     for j in range(self.state.agent.vision_range*2+1):
        #         vision_data[i].append(self.state.greatest_WO_id + 1)   #vision data (ids of the world objects in the agent's vision range)
        self.observation_space = spaces.Dict({
            "vision_data": spaces.MultiDiscrete(np.full(((self.state.agent.vision_range*2+1) * (self.state.agent.vision_range*2+1), ), self.state.greatest_WO_id + 1)),   #vision data (ids of the world objects in the agent's vision range)
            "agent_position": spaces.MultiDiscrete([self.state.world.height * self.state.world.chunk_size, self.state.world.length * self.state.world.chunk_size]),   #agent's coordinates in the map
            "standing_on": spaces.Discrete(self.state.greatest_WO_id + 1),   #id of the world object the agent is currently standing on
            "health": spaces.Discrete(self.state.agent.max_health + 1),    #agent's health
            "stamina": spaces.Discrete(self.state.agent.max_stamina + 1),   #agent's stamina
            "hunger": spaces.Discrete(self.state.agent.max_hunger + 1),   #agent's hunger
            "thirst": spaces.Discrete(self.state.agent.max_thirst + 1),   #agent's thirst
            "status": spaces.MultiBinary(len(self.state.agent.possible_status_effects)),   #agent's status effects (binary vector indicating whether the agent is affected by each possible status effect)
            "inventory": spaces.MultiDiscrete(np.full((Agent.max_inventory_space,), self.state.greatest_WO_id + 1)),   #ids of the world objects in the agent's inventory
            "inventory_space_used": spaces.Discrete(Agent.max_inventory_space + 1),   #agent's used inventory space
            "item_in_hand": spaces.Discrete(self.state.greatest_WO_id + 1),   #id of the world object the agent is currently holding in their hand (or -1 if empty)
            "possible_actions": spaces.MultiBinary(self.state.greatest_action_id + 1)   #binary vector indicating which actions are currently possible for the agent to perform (based on the current state and the agent's inventory and status)
        })
        
    # Mapeia estado atual na estrutura do espaço observacional (observação do agente do ambiente do problema)
    def observation(self) -> dict[str, Any]:
        UpdateVision().action(self.state) #update the agent vision
        inventory = np.full((Agent.max_inventory_space,), 0)
        for i in range(len(self.state.agent.inventory)):
            inventory[i] = self.state.agent.inventory[i].id
        possible_actions = np.full((self.state.greatest_action_id + 1,), 0, np.int8)
        for action_id in self.state.agent.possible_actions:
            possible_actions[action_id] = 1
        obs = {
            "vision_data": np.array(self.state.agent.id_vision_data).flatten(),   #vision data (ids of the world objects in the agent's vision range)
            "agent_position": np.array(self.state.agent.position),   #agent's coordinates in the map
            "standing_on": self.state.agent.standing_on.id,   #id of the world object the agent is currently standing on
            "health": max(self.state.agent.health, 0),   #agent's health
            "stamina": self.state.agent.stamina,   #agent's stamina
            "hunger": self.state.agent.hunger,   #agent's hunger
            "thirst": self.state.agent.thirst,   #agent's thirst
            "status": np.array(self.state.agent.status, dtype=np.int8),   #agent's status effects (binary vector indicating whether the agent is affected by each possible status effect)
            "inventory": inventory,   #ids of the world objects in the agent's inventory
            "inventory_space_used": self.state.agent.inventory_space_used,   #agent's used inventory space
            "item_in_hand": self.state.agent.item_in_hand.id if self.state.agent.item_in_hand else 0,   #id of the world object the agent is currently holding in their hand (or -1 if empty)
            "possible_actions": possible_actions   #binary vector indicating which actions are currently possible for the agent to perform (based on the current state and the agent's inventory and status)
        }
        return obs

    # Método usado para iniciar uma nova simulação a partir de um estado inicial até o turno do agente
    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[Any, dict[str, Any]]:
        super().reset(seed=seed)    #what does this do???
        self.state.reset(seed=self.seed, player_controlled=False, time_limit=self.time_limit)
        # O segundo argumento refere-se a alguma informação adicional repassada para o agente
        return self.observation(), dict()

    # Método usado para executar uma transição de estado a partir de uma ação do agente
    def step(self, action: int) -> tuple[dict[str, Any], SupportsFloat, bool, bool, dict[str, Any]]:
        reward = 0
        self.state.current_action_id = action   #store the current action id in the state for access in actions
        current_action = self.state.get_action(action)
        action_duration = current_action.duration # type: ignore
        reward = current_action.action(self.state) # type: ignore
        if reward == self.state.invalid_return_value:
            return self.observation(), reward, False, False, {"is_success": False}   #is success???
        
        oldAgentHealth = self.state.agent.health
        oldZombiesKilled = self.state.zombies_killed
        
        for _ in range(action_duration):
            self.state.time_elapsed += 1
            for zombie in self.state.zombies:
                zombie.zombie_action(self.state)
            if self.state.agent.health <= 0:
                # print("You died of a zombie attack.")
                reward += self.state.entity_death(self.state.agent)
                break
                
            #status handler (status, hunger, thirst)
            self.state.agent.hunger = min(self.state.agent.max_hunger, self.state.agent.hunger + self.state.hunger_per_time)
            self.state.agent.thirst = min(self.state.agent.max_thirst, self.state.agent.thirst + self.state.thirst_per_time)
            #apply status, then check if status is done, then add new status
            # agentStatus = [
            #     0, thirsty
            #     0, hungry
            #     0, bleeding
            #     0  tired
            # ]
            if self.state.agent.hunger >= self.state.hunger_threshold:
                self.state.agent.status[1] = 1
            if self.state.agent.thirst >= self.state.thirst_threshold:
                self.state.agent.status[0] = 1
            if self.state.agent.stamina <= 0:
                self.state.agent.status[3] = 1
                
            if self.state.agent.status[0] == 0 and self.state.agent.status[1] == 0:
                self.state.agent.stamina = min(self.state.agent.max_stamina, self.state.agent.stamina + self.state.stamina_per_time)
                
            if self.state.agent.status[1] == 1:
                self.state.agent.health -= self.state.hunger_damage
                # print("You are dying of hunger.")
                if self.state.agent.health <= 0:
                    # print("You died of hunger.")
                    reward += self.state.entity_death(self.state.agent)
                    break
            if self.state.agent.status[0] == 1:
                self.state.agent.health -= self.state.thirst_damage
                # print("You are dying of thirst.")
                if self.state.agent.health <= 0:
                    # print("You died of thirst.")
                    reward += self.state.entity_death(self.state.agent)
                    break
            if self.state.agent.status[2] > 0:
                self.state.agent.health -= self.state.bleeding_damage
                self.state.agent.status[2] -= 1
                # print("You are bleeding to death.")
                if self.state.agent.health <= 0:
                    # print("You died of bleeding.")
                    reward += self.state.entity_death(self.state.agent)
                    break
            if self.state.agent.stamina > 30:
                self.state.agent.status[3] = 0
            
            #wave handler
            if len(self.state.zombies) < self.state.world.wave_size * self.state.wave_count * 0.2:
                self.state.wave_count += 1
                self.state.world.generate_wave(self.state)
                
        reward += (self.state.agent.health - oldAgentHealth)
        reward += (self.state.zombies_killed - oldZombiesKilled) * 50
        reward -= self.state.agent.status[0] * 10  #thirsty
        reward -= self.state.agent.status[1] * 10  #hungry
        reward -= self.state.agent.status[2] * 20  #bleeding
        reward -= self.state.agent.status[3] * 5  #tired
        
        # Retorna uma tupla contendo:
        # a observação do próximo estado, a recompensa imediata obtida, se o estado é final,
        # se a simulação deve ser encerrada (estado inválido, mas não final) e informações adicionais
        return self.observation(), reward, self.state.time_elapsed >= self.state.time_limit or reward < -100, False, {"is_success": True}   #is success???

    # Método (opcional) que implementa interface gráfica
    def render(self) -> RenderFrame | list[RenderFrame] | None:
        # if self.render_mode == "human":
        print("\n" * 50)
        print("\nTime Elapsed:", self.state.time_elapsed)
        self.state.agent.print_agent_info(self.state)

    # Método (opcional) que encerra os recursos usados pelo ambiente ao finalizar uma simulação
    def close(self):
        pass