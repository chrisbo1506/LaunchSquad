#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cloud persistence module for the LunchSquad app.
Provides mechanisms to store and retrieve data in Streamlit Cloud environment.
"""

import json
import os
import streamlit as st

# Definiere Konstanten
DEFAULT_STORAGE_DIR = ".streamlit/storage"
DEFAULT_VOTE_FILE = ".streamlit/storage/votes.json"
DEFAULT_VOTE_COUNT_FILE = ".streamlit/storage/vote_count.json"

class CloudStorage:
    """
    Handles data persistence in Streamlit Cloud environment using both session_state and files.
    This class provides a reliable way to store data between app restarts for all users.
    """
    
    @staticmethod
    def _ensure_storage_dir():
        """Stellt sicher, dass das Speicherverzeichnis existiert."""
        os.makedirs(DEFAULT_STORAGE_DIR, exist_ok=True)
    
    @staticmethod
    def save_data(key, data):
        """
        Save data to Streamlit's session state AND to a persistent file.
        
        Args:
            key (str): The key to store the data under
            data (any): The data to store
        
        Returns:
            bool: True if successful
        """
        try:
            # Store in session_state for current session use
            st.session_state[key] = data
            
            # Ensure we can store this data in a file
            if not isinstance(data, (dict, list, str, int, float, bool)) and data is not None:
                print(f"Warnung: Typ nicht vollständig serialisierbar für {key}: {type(data)}")
                # Try to convert to appropriate structure if possible
                
            # Determine the appropriate file path
            CloudStorage._ensure_storage_dir()
            
            # Special case handling for known key types
            if key == "votes":
                file_path = DEFAULT_VOTE_FILE
            elif key == "vote_count":
                file_path = DEFAULT_VOTE_COUNT_FILE
            else:
                file_path = os.path.join(DEFAULT_STORAGE_DIR, f"{key}.json")
            
            # Save to persistent file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"Daten erfolgreich gespeichert für {key} in Datei {file_path}: {data}")
            return True
        except Exception as e:
            print(f"Fehler beim Speichern von {key}: {e}")
            return False
    
    @staticmethod
    def load_data(key, default=None):
        """
        Load data from session state and file-based storage.
        
        Args:
            key (str): The key to retrieve data from
            default (any): Default value if key doesn't exist
        
        Returns:
            any: The stored data or default value
        """
        try:
            # First, check session state for current session data
            if key in st.session_state:
                data = st.session_state[key]
                if data is not None:
                    print(f"Daten aus session_state geladen für {key}: {data}")
                    return data
            
            # Determine the appropriate file path
            if key == "votes":
                file_path = DEFAULT_VOTE_FILE
            elif key == "vote_count":
                file_path = DEFAULT_VOTE_COUNT_FILE
            else:
                file_path = os.path.join(DEFAULT_STORAGE_DIR, f"{key}.json")
            
            # Try to load from persistent file
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Update session state for future access
                    st.session_state[key] = data
                    print(f"Daten aus Datei geladen für {key} ({file_path}): {data}")
                    return data
                except json.JSONDecodeError:
                    print(f"Fehler beim Parsen der JSON-Datei für {key} ({file_path})")
                except Exception as e:
                    print(f"Fehler beim Laden aus Datei für {key} ({file_path}): {e}")
            
            # No data found, return default
            print(f"Keine Daten gefunden für {key}, verwende Standard: {default}")
            return default
        except Exception as e:
            print(f"Fehler beim Laden von {key}: {e}")
            return default
    
    @staticmethod
    def delete_data(key):
        """
        Delete data from both session state and file storage.
        
        Args:
            key (str): The key to delete
        
        Returns:
            bool: True if deletion was successful
        """
        try:
            success = False
            
            # Remove from session state
            if key in st.session_state:
                del st.session_state[key]
                success = True
            
            # Determine the appropriate file path
            if key == "votes":
                file_path = DEFAULT_VOTE_FILE
            elif key == "vote_count":
                file_path = DEFAULT_VOTE_COUNT_FILE
            else:
                file_path = os.path.join(DEFAULT_STORAGE_DIR, f"{key}.json")
            
            # Remove file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)
                success = True
                print(f"Datei gelöscht für {key}: {file_path}")
            
            print(f"Daten für {key} erfolgreich gelöscht")
            return success
        except Exception as e:
            print(f"Fehler beim Löschen von {key}: {e}")
            return False
    
    @staticmethod
    def list_keys():
        """
        List all persisted data keys.
        
        Returns:
            list: List of key names
        """
        keys = []
        
        # Get keys from session state
        for key in st.session_state:
            if not key.startswith('_') and key not in ['current_view', 'selected_shop', 'confirm_clear_all_main']:
                keys.append(key)
        
        # Get keys from storage directory
        try:
            if os.path.exists(DEFAULT_STORAGE_DIR):
                for filename in os.listdir(DEFAULT_STORAGE_DIR):
                    if filename.endswith('.json'):
                        key = filename[:-5]  # Remove .json extension
                        if key not in keys:
                            keys.append(key)
        except Exception as e:
            print(f"Fehler beim Auflisten der Dateien im Speicherverzeichnis: {e}")
        
        return keys