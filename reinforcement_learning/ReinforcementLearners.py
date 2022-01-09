import torch
import numpy as np
from abc import ABC, abstractmethod
from torch.autograd import Variable
from utils.reinforcement_learning_utils import PolicyNet, Categorical, plot_durations
from game.gym import WordleGym
from typing import List


class WordleRL(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def make_model(self, *args):
        pass

    @abstractmethod
    def convert_state_to_feature(self, *args) -> torch.Tensor:
        pass

    @abstractmethod
    def convert_model_action_to_game_action(self, *args):
        pass

    @abstractmethod
    def train(self, *args):
        pass


class SimpleWordlePolicyRL(WordleRL, ABC):
    def __init__(self, action_space_size: int, state_space_size: int):
        super().__init__()
        self.action_space_size = action_space_size
        self.state_space_size = state_space_size
        self.model = self.make_model()

    def make_model(self):
        return PolicyNet((self.state_space_size,), self.action_space_size)

    def convert_state_to_feature(self, state: List[str], corpus: List[str]) -> torch.Tensor:
        """

        :param corpus: list of words total
        :param state: the list of words we can pick
        :return: binary tensor where words we can pick from  = 1, words we cant = 0
        """
        n = len(corpus)
        feature_vec = np.zeros((n, 1))
        keep_indices = [corpus.index(word) for word in state]
        feature_vec[keep_indices, :] = 1

        return torch.from_numpy(feature_vec.T).float()

    def convert_model_action_to_game_action(self, model_action: torch.Tensor) -> int:
        """

        :param model_action: 1,1 torch tensor integer
        :param corpus: list of words
        :return: string of action
        """
        return model_action.item()

    def train(self, gamma: float, learning_rate: float, num_episodes: int, batch_size: int,
              gym_env: WordleGym, time_horizon: int) -> PolicyNet:
        """

        :param gym_env: which env are we in
        :param gamma: discount factor
        :param learning_rate: selfexplanatory
        :param num_episodes: how many games to play
        :param batch_size: size of games to stop at
        :param time_horizon: number of guess you can make
        :return: trained model
        """

        episode_durations = []
        optimizer = torch.optim.RMSprop(self.model.parameters(), lr=learning_rate)

        # Batch History
        state_pool = []
        action_pool = []
        reward_pool = []
        steps = 0

        for e in range(num_episodes):

            gym_env.reset()
            state = gym_env.corpus
            state = Variable(self.convert_state_to_feature(state, gym_env.corpus))

            for t in range(time_horizon):
                probs = self.model(state)
                m = Categorical(probs)
                action = m.sample()

                action = self.convert_model_action_to_game_action(action)
                next_state, reward, done, round_info = gym_env.step(action)

                # To mark boundarys between episodes
                if done:
                    if round_info["result"]:
                        reward = 10 / t

                state_pool.append(state)
                action_pool.append(action)
                reward_pool.append(reward)

                state = next_state
                state = Variable(self.convert_state_to_feature(state, gym_env.corpus))

                steps += 1

                if done:
                    episode_durations.append(t + 1)
                    # plot_durations(episode_durations)
                    break

            # Update policy
            if e > 0 and e % batch_size == 0:

                # Discount reward
                running_add = 0
                for i in reversed(range(steps)):
                    running_add = running_add * gamma + reward_pool[i]
                    reward_pool[i] = running_add

                # Normalize reward
                reward_mean = np.mean(reward_pool)
                reward_std = np.std(reward_pool)
                for i in range(steps):
                    reward_pool[i] = (reward_pool[i] - reward_mean) / reward_std

                # Gradient Desent
                optimizer.zero_grad()

                for i in range(steps):
                    state = state_pool[i]
                    action = Variable(torch.FloatTensor([action_pool[i]]))
                    reward = reward_pool[i]

                    probs = self.model(state)
                    m = Categorical(probs)
                    loss = -m.log_prob(action) * reward  # Negtive score function x reward
                    loss.backward()

                optimizer.step()

                state_pool = []
                action_pool = []
                reward_pool = []
                steps = 0
        return self.model
