from abc import ABC
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple, List
from torch.distributions.categorical import Categorical
from torch import einsum
from einops import reduce


def plot_durations(episode_durations: List[int]):
    """

    :param episode_durations: duration of episodes
    :return:
    """
    plt.figure(2)
    plt.clf()
    durations_t = torch.FloatTensor(episode_durations)
    plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(durations_t.numpy())
    # Take 100 episode averages and plot them too
    if len(durations_t) >= 100:
        means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(99), means))
        plt.plot(means.numpy())

    plt.pause(0.001)  # pause a bit so that plots are updated


class PolicyNet(nn.Module):
    def __init__(self, input_dim: Tuple[int], output_dim):
        super(PolicyNet, self).__init__()

        self.fc1 = nn.Linear(*input_dim, 24)
        self.fc2 = nn.Linear(24, 36)
        self.fc3 = nn.Linear(36, output_dim)  # Prob of word choice

    def forward(self, input_x):
        mask = input_x
        x = F.relu(self.fc1(input_x))
        x = F.relu(self.fc2(x))
        x = CategoricalMasked(self.fc3(x),mask.bool())
        return x.probs


class CategoricalMasked(Categorical, ABC):

    def __init__(self, logits: torch.Tensor, mask: Optional[torch.Tensor] = None):
        self.mask = mask
        self.batch, self.nb_action = logits.size()
        if mask is None:
            super(CategoricalMasked, self).__init__(logits=logits)
        else:
            self.mask_value = torch.finfo(logits.dtype).min
            logits.masked_fill_(~self.mask, self.mask_value)
            super(CategoricalMasked, self).__init__(logits=logits)

    def entropy(self):
        if self.mask is None:
            return super().entropy()
        # Elementwise multiplication
        p_log_p = einsum("ij,ij->ij", self.logits, self.probs)
        # Compute the entropy with possible action only
        p_log_p = torch.where(
            self.mask,
            p_log_p,
            torch.tensor(0, dtype=p_log_p.dtype, device=p_log_p.device),
        )
        return -reduce(p_log_p, "b a -> b", "sum", b=self.batch, a=self.nb_action)
