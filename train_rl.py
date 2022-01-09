import torch
from reinforcement_learning.ReinforcementLearners import SimpleWordlePolicyRL
from game.gym import WordleGym
from utils.utils import english_dictionary

if __name__ == "__main__":
    num_episodes = 100000
    learning_rate = .001
    gamma = .99
    batch_size = 10
    time_horizon = 6
    action_space_size = len(english_dictionary)

    gym_env = WordleGym(time_horizon, corpus=english_dictionary)
    rl_model = SimpleWordlePolicyRL(action_space_size=action_space_size, state_space_size=action_space_size)

    rl_model.train(gamma=gamma, learning_rate=learning_rate, num_episodes=num_episodes, batch_size=batch_size,
                   gym_env=gym_env,
                   time_horizon=time_horizon)

    torch.save(rl_model.model, "saved_models/simple_rl_model.pth")

