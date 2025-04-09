#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cloud persistence module for the LunchSquad app.
Provides mechanisms to store and retrieve data in Streamlit Cloud environment.
"""

import json
import pickle
import base64
import streamlit as st

class CloudStorage:
    """
    Handles data persistence in Streamlit Cloud environment using session_state and cookies.
    This class provides a reliable way to store data between app restarts in Streamlit Cloud.
    """
    
    # Prefix for cookie-based storage
    COOKIE_PREFIX = "stpersist_"
    
    @staticmethod
    def save_data(key, data):
        """
        Save data to Streamlit's session state and cookies for persistent storage.
        
        Args:
            key (str): The key to store the data under
            data (any): The data to store
        
        Returns:
            bool: True if successful
        """
        try:
            # Store in session_state for current session use
            st.session_state[key] = data
            
            # Handle data serialization for cookie storage
            if isinstance(data, (dict, list)):
                # For complex types, use JSON serialization
                serialized_data = json.dumps(data)
            else:
                # For simple types, convert to string
                serialized_data = str(data)
            
            # Use st.experimental_set_query_params to create a persistent URL parameter
            # This acts like a cookie that persists between sessions
            cookie_key = f"{CloudStorage.COOKIE_PREFIX}{key}"
            
            # Create or update our special URL parameter
            # We're abusing query parameters as a persistent storage mechanism
            st.query_params[cookie_key] = serialized_data
            
            # Also store directly as a cookie if supporting browser storage
            # This is a backup method and might not work in all environments
            st.markdown(
                f"""
                <script>
                    localStorage.setItem('{cookie_key}', '{serialized_data}');
                    console.log('Stored data for {key}');
                </script>
                """,
                unsafe_allow_html=True
            )
            
            print(f"Daten erfolgreich gespeichert für {key}: {data}")
            return True
        except Exception as e:
            print(f"Fehler beim Speichern von {key}: {e}")
            return False
    
    @staticmethod
    def load_data(key, default=None):
        """
        Load data from Streamlit's persistent storage mechanisms.
        
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
            
            # Check URL parameters (our abuse of query params for persistence)
            cookie_key = f"{CloudStorage.COOKIE_PREFIX}{key}"
            
            if cookie_key in st.query_params:
                serialized_data = st.query_params[cookie_key]
                
                # Try to parse as JSON for complex types
                try:
                    data = json.loads(serialized_data)
                    st.session_state[key] = data  # Update session state
                    print(f"Daten aus URL-Parametern geladen für {key}: {data}")
                    return data
                except json.JSONDecodeError:
                    # If not JSON, use as string or convert appropriately
                    st.session_state[key] = serialized_data
                    print(f"Daten als String aus URL-Parametern geladen für {key}: {serialized_data}")
                    return serialized_data
            
            # Also try to load from local storage in the browser
            # This might not execute in all environments 
            local_storage_check = st.empty()
            local_storage_check.markdown(
                f"""
                <script>
                    const storedData = localStorage.getItem('{cookie_key}');
                    if (storedData) {{
                        console.log('Found data in localStorage for {key}');
                        window.parent.postMessage({{
                            type: 'streamlit:setComponentValue',
                            value: storedData
                        }}, '*');
                    }}
                </script>
                """,
                unsafe_allow_html=True
            )
            
            # No data found in any storage, return default
            print(f"Keine Daten gefunden für {key}, verwende Standard: {default}")
            return default
        except Exception as e:
            print(f"Fehler beim Laden von {key}: {e}")
            return default
    
    @staticmethod
    def delete_data(key):
        """
        Delete data from all storage mechanisms.
        
        Args:
            key (str): The key to delete
        
        Returns:
            bool: True if deletion was successful
        """
        try:
            # Remove from session state
            if key in st.session_state:
                del st.session_state[key]
            
            # Remove from URL parameters
            cookie_key = f"{CloudStorage.COOKIE_PREFIX}{key}"
            if cookie_key in st.query_params:
                del st.query_params[cookie_key]
            
            # Try to remove from local storage
            st.markdown(
                f"""
                <script>
                    localStorage.removeItem('{cookie_key}');
                    console.log('Removed data for {key}');
                </script>
                """,
                unsafe_allow_html=True
            )
            
            print(f"Daten für {key} erfolgreich gelöscht")
            return True
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
        
        # Get keys from URL parameters
        for param_key in st.query_params:
            if param_key.startswith(CloudStorage.COOKIE_PREFIX):
                # Extract the original key name
                original_key = param_key[len(CloudStorage.COOKIE_PREFIX):]
                if original_key not in keys:
                    keys.append(original_key)
        
        return keys