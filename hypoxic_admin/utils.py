"""Utilities for Hypoxic Admin"""


def jwt_get_secret_key(user_model):
    """Helper function to return jwt_secret"""
    return user_model.jwt_secret
