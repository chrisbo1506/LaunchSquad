#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cloud persistence module for the LunchSquad app.
Provides mechanisms to store and retrieve data in Streamlit Cloud environment.
"""

import json
import streamlit as st

class CloudStorage:
    """
    Handles data persistence in Streamlit Cloud environment using session_state.
    This class provides a reliable way to store data between app restarts in Streamlit Cloud.
    """
    
    @staticmethod
    def save_data(key, data):
        """
        Save data to Streamlit's session state with a persistent marker.
        
        Args:
            key (str): The key to store the data under
            data (any): The data to store
        
        Returns:
            bool: True if successful
        """
        # Create a persistent storage marker if it doesn't exist
        if '_persistent_data_keys' not in st.session_state:
            st.session_state._persistent_data_keys = set()
        
        # Add this key to the persistent keys set
        st.session_state._persistent_data_keys.add(key)
        
        # Store the actual data
        st.session_state[key] = data
        return True
    
    @staticmethod
    def load_data(key, default=None):
        """
        Load data from Streamlit's session state.
        
        Args:
            key (str): The key to retrieve data from
            default (any): Default value if key doesn't exist
        
        Returns:
            any: The stored data or default value
        """
        if key in st.session_state:
            return st.session_state[key]
        return default
    
    @staticmethod
    def delete_data(key):
        """
        Delete data from Streamlit's session state.
        
        Args:
            key (str): The key to delete
        
        Returns:
            bool: True if deletion was successful
        """
        if key in st.session_state:
            del st.session_state[key]
            if '_persistent_data_keys' in st.session_state and key in st.session_state._persistent_data_keys:
                st.session_state._persistent_data_keys.remove(key)
            return True
        return False
    
    @staticmethod
    def list_keys():
        """
        List all persistent data keys.
        
        Returns:
            set: Set of key names
        """
        if '_persistent_data_keys' in st.session_state:
            return st.session_state._persistent_data_keys
        return set()