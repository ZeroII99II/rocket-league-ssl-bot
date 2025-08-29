#!/usr/bin/env python3
"""
Modern Agent Architecture for RLGym 2.0.1
State-of-the-art neural network architecture for SSL-level performance
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Any, Dict, List, Optional, Tuple
import math

class ModernAgent(nn.Module):
    """
    Modern agent architecture with SSL-level features:
    - Multi-head attention for opponent modeling
    - Transformer-based observation processing
    - Specialized sub-networks for different mechanics
    - Advanced action distribution modeling
    - Temporal sequence processing
    - Hierarchical decision making
    """
    
    def __init__(self, 
                 obs_size: int = 107,
                 action_size: int = 8,
                 hidden_size: int = 512,
                 num_heads: int = 8,
                 num_layers: int = 6,
                 dropout: float = 0.1,
                 use_attention: bool = True,
                 use_transformer: bool = True,
                 use_specialized_heads: bool = True,
                 use_temporal_modeling: bool = True,
                 use_hierarchical: bool = True):
        
        super().__init__()
        
        self.obs_size = obs_size
        self.action_size = action_size
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.dropout = dropout
        self.use_attention = use_attention
        self.use_transformer = use_transformer
        self.use_specialized_heads = use_specialized_heads
        self.use_temporal_modeling = use_temporal_modeling
        self.use_hierarchical = use_hierarchical
        
        # Input processing
        self.input_norm = nn.LayerNorm(obs_size)
        self.input_projection = nn.Linear(obs_size, hidden_size)
        
        # Transformer encoder for observation processing
        if self.use_transformer:
            encoder_layer = nn.TransformerEncoderLayer(
                d_model=hidden_size,
                nhead=num_heads,
                dim_feedforward=hidden_size * 4,
                dropout=dropout,
                activation='gelu',
                batch_first=True
            )
            self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers)
        
        # Multi-head attention for opponent modeling
        if self.use_attention:
            self.attention = nn.MultiheadAttention(
                embed_dim=hidden_size,
                num_heads=num_heads,
                dropout=dropout,
                batch_first=True
            )
        
        # Temporal modeling with LSTM
        if self.use_temporal_modeling:
            self.temporal_encoder = nn.LSTM(
                input_size=hidden_size,
                hidden_size=hidden_size,
                num_layers=2,
                dropout=dropout,
                batch_first=True
            )
        
        # Hierarchical decision making
        if self.use_hierarchical:
            self.hierarchy_selector = nn.Sequential(
                nn.Linear(hidden_size, hidden_size // 2),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_size // 2, 10),  # 10 sub-models
                nn.Softmax(dim=-1)
            )
        
        # Specialized sub-networks for different mechanics
        if self.use_specialized_heads:
            self.specialized_heads = nn.ModuleDict({
                'kickoff': self._create_specialized_head(hidden_size, action_size),
                'ground_play': self._create_specialized_head(hidden_size, action_size),
                'aerial': self._create_specialized_head(hidden_size, action_size),
                'flick_bump': self._create_specialized_head(hidden_size, action_size),
                'flip_reset': self._create_specialized_head(hidden_size, action_size),
                'recovery': self._create_specialized_head(hidden_size, action_size),
                'wall_play': self._create_specialized_head(hidden_size, action_size),
                'double_tap': self._create_specialized_head(hidden_size, action_size),
                'boost_management': self._create_specialized_head(hidden_size, action_size),
                'team_play': self._create_specialized_head(hidden_size, action_size)
            })
        
        # Main policy network
        self.policy_network = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, action_size)
        )
        
        # Value network
        self.value_network = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, 1)
        )
        
        # Action distribution parameters
        self.action_std = nn.Parameter(torch.ones(action_size) * 0.1)
        
        # Initialize weights
        self._initialize_weights()
        
    def _create_specialized_head(self, input_size: int, output_size: int) -> nn.Module:
        """Create a specialized head for a specific mechanic"""
        return nn.Sequential(
            nn.Linear(input_size, input_size // 2),
            nn.ReLU(),
            nn.Dropout(self.dropout),
            nn.Linear(input_size // 2, input_size // 4),
            nn.ReLU(),
            nn.Dropout(self.dropout),
            nn.Linear(input_size // 4, output_size)
        )
    
    def _initialize_weights(self):
        """Initialize network weights"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.LayerNorm):
                nn.init.ones_(module.weight)
                nn.init.zeros_(module.bias)
    
    def forward(self, obs: torch.Tensor, hidden_state: Optional[Tuple[torch.Tensor, torch.Tensor]] = None) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """
        Forward pass through the network
        
        Args:
            obs: Observation tensor [batch_size, seq_len, obs_size]
            hidden_state: Previous hidden state for LSTM
            
        Returns:
            action_mean: Mean action values
            action_std: Action standard deviations
            value: State value
            new_hidden_state: New hidden state for LSTM
        """
        # Handle both 2D and 3D input tensors
        if len(obs.shape) == 2:
            # Add sequence dimension for 2D input
            obs = obs.unsqueeze(1)  # (batch_size, 1, features)
        
        batch_size, seq_len, _ = obs.shape
        
        # Input processing
        obs_norm = self.input_norm(obs)
        x = self.input_projection(obs_norm)
        
        # Transformer encoding
        if self.use_transformer:
            x = self.transformer_encoder(x)
        
        # Multi-head attention for opponent modeling
        if self.use_attention:
            attn_output, _ = self.attention(x, x, x)
            x = x + attn_output  # Residual connection
        
        # Temporal modeling
        if self.use_temporal_modeling:
            x, new_hidden_state = self.temporal_encoder(x, hidden_state)
        else:
            new_hidden_state = None
        
        # Use the last timestep for decision making
        x = x[:, -1, :]  # [batch_size, hidden_size]
        
        # Hierarchical decision making
        if self.use_hierarchical:
            hierarchy_weights = self.hierarchy_selector(x)
            
            # Combine specialized heads based on hierarchy weights
            specialized_outputs = []
            for i, (head_name, head) in enumerate(self.specialized_heads.items()):
                head_output = head(x)
                weighted_output = head_output * hierarchy_weights[:, i:i+1]
                specialized_outputs.append(weighted_output)
            
            # Combine all specialized outputs
            combined_output = torch.sum(torch.stack(specialized_outputs, dim=1), dim=1)
            
            # Add to main policy
            main_policy = self.policy_network(x)
            action_mean = main_policy + combined_output
        else:
            action_mean = self.policy_network(x)
        
        # Value estimation
        value = self.value_network(x)
        
        # Action distribution
        action_std = F.softplus(self.action_std) + 1e-5
        
        return action_mean, action_std, value, new_hidden_state
    
    def get_action(self, obs: torch.Tensor, hidden_state: Optional[Tuple[torch.Tensor, torch.Tensor]] = None, deterministic: bool = False) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """
        Get action from the network
        
        Args:
            obs: Observation tensor
            hidden_state: Previous hidden state
            deterministic: Whether to use deterministic actions
            
        Returns:
            action: Sampled action
            log_prob: Log probability of the action
            value: State value
            new_hidden_state: New hidden state
        """
        action_mean, action_std, value, new_hidden_state = self.forward(obs, hidden_state)
        
        # Create action distribution
        action_dist = torch.distributions.Normal(action_mean, action_std)
        
        if deterministic:
            action = action_mean
        else:
            action = action_dist.sample()
        
        log_prob = action_dist.log_prob(action).sum(dim=-1)
        
        return action, log_prob, value, new_hidden_state
    
    def evaluate_actions(self, obs: torch.Tensor, actions: torch.Tensor, hidden_state: Optional[Tuple[torch.Tensor, torch.Tensor]] = None) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Evaluate actions for training
        
        Args:
            obs: Observation tensor
            actions: Actions to evaluate
            hidden_state: Previous hidden state
            
        Returns:
            log_prob: Log probability of actions
            value: State value
            entropy: Action entropy
            new_hidden_state: New hidden state
        """
        action_mean, action_std, value, new_hidden_state = self.forward(obs, hidden_state)
        
        # Create action distribution
        action_dist = torch.distributions.Normal(action_mean, action_std)
        
        log_prob = action_dist.log_prob(actions).sum(dim=-1)
        entropy = action_dist.entropy().sum(dim=-1)
        
        return log_prob, value, entropy, new_hidden_state

class ModernSelector(nn.Module):
    """
    Modern selector network for choosing between specialized sub-models
    """
    
    def __init__(self, 
                 obs_size: int = 107,
                 num_submodels: int = 10,
                 hidden_size: int = 256,
                 dropout: float = 0.1):
        
        super().__init__()
        
        self.obs_size = obs_size
        self.num_submodels = num_submodels
        self.hidden_size = hidden_size
        
        # Feature extraction
        self.feature_extractor = nn.Sequential(
            nn.Linear(obs_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        # Context encoder
        self.context_encoder = nn.Sequential(
            nn.Linear(hidden_size // 2, hidden_size // 4),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 4, hidden_size // 8),
            nn.ReLU()
        )
        
        # Sub-model selector
        self.selector = nn.Sequential(
            nn.Linear(hidden_size // 2 + hidden_size // 8, hidden_size // 4),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 4, num_submodels),
            nn.Softmax(dim=-1)
        )
        
        # Confidence estimator
        self.confidence = nn.Sequential(
            nn.Linear(hidden_size // 2 + hidden_size // 8, hidden_size // 4),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 4, 1),
            nn.Sigmoid()
        )
        
    def forward(self, obs: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass through the selector
        
        Args:
            obs: Observation tensor
            
        Returns:
            submodel_weights: Weights for each sub-model
            confidence: Confidence in the selection
        """
        # Extract features
        features = self.feature_extractor(obs)
        
        # Encode context
        context = self.context_encoder(features)
        
        # Combine features and context
        combined = torch.cat([features, context], dim=-1)
        
        # Select sub-model
        submodel_weights = self.selector(combined)
        
        # Estimate confidence
        confidence = self.confidence(combined)
        
        return submodel_weights, confidence

class ModernMultiDiscretePolicy(nn.Module):
    """
    Modern multi-discrete policy for complex action spaces
    """
    
    def __init__(self, 
                 obs_size: int = 107,
                 action_dims: List[int] = [5, 5, 3, 12],
                 hidden_size: int = 512,
                 dropout: float = 0.1):
        
        super().__init__()
        
        self.obs_size = obs_size
        self.action_dims = action_dims
        self.hidden_size = hidden_size
        self.num_actions = len(action_dims)
        
        # Shared feature extractor
        self.feature_extractor = nn.Sequential(
            nn.Linear(obs_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        # Action-specific heads
        self.action_heads = nn.ModuleList([
            nn.Sequential(
                nn.Linear(hidden_size // 2, hidden_size // 4),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_size // 4, dim)
            ) for dim in action_dims
        ])
        
        # Value head
        self.value_head = nn.Sequential(
            nn.Linear(hidden_size // 2, hidden_size // 4),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 4, 1)
        )
        
    def forward(self, obs: torch.Tensor) -> Tuple[List[torch.Tensor], torch.Tensor]:
        """
        Forward pass through the policy
        
        Args:
            obs: Observation tensor
            
        Returns:
            action_logits: Logits for each action dimension
            value: State value
        """
        # Extract features
        features = self.feature_extractor(obs)
        
        # Get action logits
        action_logits = []
        for head in self.action_heads:
            logits = head(features)
            action_logits.append(logits)
        
        # Get value
        value = self.value_head(features)
        
        return action_logits, value
    
    def get_action(self, obs: torch.Tensor, deterministic: bool = False) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Get action from the policy
        
        Args:
            obs: Observation tensor
            deterministic: Whether to use deterministic actions
            
        Returns:
            action: Sampled action
            log_prob: Log probability of the action
            value: State value
        """
        action_logits, value = self.forward(obs)
        
        # Sample actions
        actions = []
        log_probs = []
        
        for i, logits in enumerate(action_logits):
            dist = torch.distributions.Categorical(logits=logits)
            
            if deterministic:
                action = torch.argmax(logits, dim=-1)
            else:
                action = dist.sample()
            
            log_prob = dist.log_prob(action)
            
            actions.append(action)
            log_probs.append(log_prob)
        
        # Combine actions and log probabilities
        action = torch.stack(actions, dim=-1)
        log_prob = torch.stack(log_probs, dim=-1).sum(dim=-1)
        
        return action, log_prob, value
    
    def evaluate_actions(self, obs: torch.Tensor, actions: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Evaluate actions for training
        
        Args:
            obs: Observation tensor
            actions: Actions to evaluate
            
        Returns:
            log_prob: Log probability of actions
            value: State value
            entropy: Action entropy
        """
        action_logits, value = self.forward(obs)
        
        # Evaluate actions
        log_probs = []
        entropies = []
        
        for i, (logits, action) in enumerate(zip(action_logits, actions.unbind(dim=-1))):
            dist = torch.distributions.Categorical(logits=logits)
            log_prob = dist.log_prob(action)
            entropy = dist.entropy()
            
            log_probs.append(log_prob)
            entropies.append(entropy)
        
        # Combine log probabilities and entropies
        log_prob = torch.stack(log_probs, dim=-1).sum(dim=-1)
        entropy = torch.stack(entropies, dim=-1).sum(dim=-1)
        
        return log_prob, value, entropy

# Legacy compatibility classes
class Opti(ModernAgent):
    """Legacy compatibility class for existing code"""
    
    def __init__(self, **kwargs):
        obs_size = kwargs.get('obs_size', 107)
        action_size = kwargs.get('action_size', 8)
        hidden_size = kwargs.get('hidden_size', 512)
        
        super().__init__(
            obs_size=obs_size,
            action_size=action_size,
            hidden_size=hidden_size,
            use_attention=True,
            use_transformer=True,
            use_specialized_heads=True,
            use_temporal_modeling=True,
            use_hierarchical=True
        )

class OptiSelector(ModernSelector):
    """Legacy compatibility class for existing code"""
    
    def __init__(self, **kwargs):
        obs_size = kwargs.get('obs_size', 107)
        num_submodels = kwargs.get('num_submodels', 10)
        hidden_size = kwargs.get('hidden_size', 256)
        
        super().__init__(
            obs_size=obs_size,
            num_submodels=num_submodels,
            hidden_size=hidden_size
        )

class MultiDiscretePolicy(ModernMultiDiscretePolicy):
    """Legacy compatibility class for existing code"""
    
    def __init__(self, **kwargs):
        obs_size = kwargs.get('obs_size', 107)
        action_dims = kwargs.get('action_dims', [5, 5, 3, 12])
        hidden_size = kwargs.get('hidden_size', 512)
        
        super().__init__(
            obs_size=obs_size,
            action_dims=action_dims,
            hidden_size=hidden_size
        )
