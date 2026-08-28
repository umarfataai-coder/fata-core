import pytest
import torch
from model.transformer import FataEngineModel
from app.memory import FataMemory

def test_fata_transformer_dimensions():
    """Gwajin tabbatar da cewa siffar Neural Network din Fata tana fitar da ma'auni daidai"""
    vocab_size = 50257
    batch_size = 2
    seq_len = 64
    
    model = FataEngineModel(vocab_size=vocab_size, embed_dim=256, num_layers=2, num_heads=4, ff_dim=512)
    dummy_input = torch.randint(0, vocab_size, (batch_size, seq_len))
    
    output = model(dummy_input)
    assert output.shape == (batch_size, seq_len, vocab_size), "Gwajin siffar Fata AI ya fadi!"

def test_redis_memory_integration(mocker):
    """Gwajin tabbatar da cewa Redis yana kiyaye tarihin tattaunawa"""
    mock_redis = mocker.patch("redis.Redis")
    memory = FataMemory()
    
    memory.save_chat_context("session_123", "Sannu Fata", "Barka kadai!")
    mock_redis.return_value.rpush.assert_called_once()