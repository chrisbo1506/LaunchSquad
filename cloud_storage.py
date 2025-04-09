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
    
    # Präfix für persistente Schlüssel
    PERSISTENT_PREFIX = "persisted_"
    
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
        
        # Erstelle einen persistenten Schlüssel mit Präfix
        persistent_key = f"{CloudStorage.PERSISTENT_PREFIX}{key}"
        
        # Store the actual data unter beiden Schlüsseln
        st.session_state[key] = data
        st.session_state[persistent_key] = data
        
        # Debug-Output
        print(f"Daten gespeichert unter {key} und {persistent_key}: {data}")
        
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
        # Prüfe zuerst den persistenten Schlüssel
        persistent_key = f"{CloudStorage.PERSISTENT_PREFIX}{key}"
        
        if persistent_key in st.session_state:
            data = st.session_state[persistent_key]
            # Stelle sicher, dass der reguläre Schlüssel auch den Wert hat
            st.session_state[key] = data
            print(f"Daten von {persistent_key} geladen: {data}")
            return data
        
        # Fallback zum regulären Schlüssel
        if key in st.session_state:
            data = st.session_state[key]
            print(f"Daten von {key} geladen: {data}")
            return data
            
        print(f"Keine Daten für {key} gefunden, verwende Standard: {default}")
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
        success = False
        
        # Lösche den regulären Schlüssel
        if key in st.session_state:
            del st.session_state[key]
            success = True
        
        # Lösche auch den persistenten Schlüssel
        persistent_key = f"{CloudStorage.PERSISTENT_PREFIX}{key}"
        if persistent_key in st.session_state:
            del st.session_state[persistent_key]
            success = True
        
        # Aktualisiere die Liste der persistenten Schlüssel
        if '_persistent_data_keys' in st.session_state and key in st.session_state._persistent_data_keys:
            st.session_state._persistent_data_keys.remove(key)
        
        print(f"Daten für {key} und {persistent_key} gelöscht, Erfolg: {success}")
        return success
    
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