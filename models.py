#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data models for the LunchSquad application
"""

import json
import os
from datetime import datetime
import pandas as pd
import streamlit as st
from config import DEFAULT_ORDER_FILE
from cloud_storage import CloudStorage

class OrderManager:
    """Manages the orders and their persistence"""

    def __init__(self, storage_file=DEFAULT_ORDER_FILE):
        self.storage_file = storage_file
        self.orders = []
        self.cloud_storage = CloudStorage()
        self.load_orders()

    def add_order(self, order):
        """Add a new order to the list"""
        # Add timestamp to the order
        order["timestamp"] = datetime.now().isoformat()
        self.orders.append(order)
        # Save immediately for persistence
        self.save_orders()
        return True

    def remove_order(self, index):
        """Remove an order by its index"""
        if 0 <= index < len(self.orders):
            del self.orders[index]
            # Save immediately for persistence
            self.save_orders()
            return True
        return False

    def clear_orders(self):
        """Clear all orders"""
        self.orders = []
        # Speichere die leere Liste, um Persistenz zu gewährleisten
        self.save_orders()
        return True

    def get_orders(self):
        """Get all orders"""
        return self.orders

    def load_orders(self):
        """
        Load orders with a hierarchical approach:
        1. First try Cloud Storage (for Streamlit Cloud)
        2. Then try session state (for compatibility with existing code)
        3. Finally try file-based storage (for local development)
        """
        # Step 1: Try Cloud Storage first (most reliable in Streamlit Cloud)
        cloud_orders = self.cloud_storage.load_data('orders_data')
        if cloud_orders is not None:
            self.orders = cloud_orders
            # Ensure session state is also updated
            if hasattr(st, 'session_state'):
                st.session_state.orders_data = self.orders
            return True
            
        # Step 2: Try session state (for compatibility with existing code)
        if hasattr(st, 'session_state') and 'orders_data' in st.session_state:
            self.orders = st.session_state.orders_data
            # Save to cloud storage for future use
            self.cloud_storage.save_data('orders_data', self.orders)
            return True
        
        # Step 3: Try file-based storage (works for local development)
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    self.orders = json.load(f)
                
                # Save to cloud storage and session state for future use
                self.cloud_storage.save_data('orders_data', self.orders)
                if hasattr(st, 'session_state'):
                    st.session_state.orders_data = self.orders
                return True
        except Exception as e:
            print(f"Error loading orders from file: {e}")
        
        # If no orders found, initialize with empty list
        self.orders = []
        self.cloud_storage.save_data('orders_data', self.orders)
        if hasattr(st, 'session_state'):
            st.session_state.orders_data = self.orders
        return False

    def save_orders(self):
        """
        Save orders with a hierarchical approach:
        1. Always save to Cloud Storage (for Streamlit Cloud persistence)
        2. Always update session state (for current session)
        3. Try to save to file (works locally, may not work on Streamlit Cloud)
        """
        # Step 1: Always save to Cloud Storage (critical for Streamlit Cloud)
        self.cloud_storage.save_data('orders_data', self.orders)
        
        # Step 2: Always update session state (for current session)
        if hasattr(st, 'session_state'):
            st.session_state.orders_data = self.orders
        
        # Step 3: Try to save to file (works locally, may not work on Streamlit Cloud)
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.orders, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: Could not save to file (expected in cloud environments): {e}")
            # This is expected to fail in some cloud environments, but we already
            # saved to Cloud Storage, so we still return True
        
        return True

    def get_orders_dataframe(self):
        """Convert orders to a pandas DataFrame for display"""
        if not self.orders:
            return pd.DataFrame()
        
        # Create a DataFrame from the orders list
        df = pd.DataFrame(self.orders)
        
        # Format the DataFrame for display
        if not df.empty:
            # Handle timestamp formatting
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['Zeitpunkt'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
            
            # Add formatted columns based on order type
            formatted_rows = []
            for _, row in df.iterrows():
                formatted_row = {}
                formatted_row['Zeitpunkt'] = row.get('Zeitpunkt', '-')
                formatted_row['Name'] = row.get('name', '-')
                
                order_type = row.get('type', '')
                if order_type == 'yamyam':
                    formatted_row['Restaurant'] = 'YamYam'
                    formatted_row['Bestellung'] = f"Nr. {row.get('number', '-')}"
                    formatted_row['Details'] = ''
                
                elif order_type == 'doner':
                    formatted_row['Restaurant'] = 'Döner'
                    
                    # Map product values to display names
                    product_map = {
                        "doner": "Döner",
                        "durum": "Dürüm",
                        "falafel-doner": "Falafel-Döner",
                        "falafel-durum": "Falafel-Dürüm",
                        "box": "Dönerbox"
                    }
                    
                    # Map shop values to display names
                    shop_map = {
                        "bruder": "Döner Bruder",
                        "king": "King Kebabo's",
                        "aldi": "Aldi Döner"
                    }
                    
                    product = product_map.get(row.get('product', ''), row.get('product', ''))
                    shop = shop_map.get(row.get('shop', ''), row.get('shop', ''))
                    
                    # Format sauces
                    sauces = row.get('sauces', [])
                    sauce_str = ", ".join(sauces) if sauces else "keine"
                    
                    # Format extras with custom extras
                    extras_list = []
                    for extra in row.get('extras', []):
                        if isinstance(extra, str) and extra.startswith("custom:"):
                            # Es ist ein Freitext-Extra
                            custom_text = extra[7:]  # "custom:" entfernen
                            extras_list.append(custom_text)
                        else:
                            # Standard-Extras wie "ohne-zwiebel" konvertieren
                            extras_map = {
                                "ohne-zwiebel": "Ohne Zwiebel",
                                "ohne-tomate": "Ohne Tomate", 
                                "ohne-blaukraut": "Ohne Blaukraut",
                                "ohne-salat": "Ohne Salat",
                                "ohne-sosse": "Ohne Soße",
                                "ohne-grillgemuese": "Ohne Grillgemüse",
                                "ohne-gurke": "Ohne Gurke"
                            }
                            extras_list.append(extras_map.get(extra, extra))
                            
                    extras_str = ", ".join(extras_list) if extras_list else "keine"
                    
                    # Box type if applicable
                    box_type = ""
                    if row.get('product') == 'box' and 'boxType' in row:
                        box_map = {"pommes": "mit Pommes", "salat": "mit Salat"}
                        box_type = f" ({box_map.get(row['boxType'], row['boxType'])})"
                    
                    # Format spice level
                    spice_map = {"none": "nicht scharf", "normal": "normal scharf", "extra": "sehr scharf"}
                    spice = spice_map.get(row.get('spiceLevel', ''), row.get('spiceLevel', ''))
                    
                    formatted_row['Bestellung'] = f"{product}{box_type} ({shop})"
                    formatted_row['Details'] = f"Soßen: {sauce_str}, Extras: {extras_str}, Schärfe: {spice}"
                
                elif order_type == 'edeka':
                    formatted_row['Restaurant'] = 'Edeka'
                    product = row.get('product', '-')
                    
                    if product == 'Salat':
                        salat_type = row.get('salatType', '-')
                        formatted_row['Bestellung'] = f"{salat_type}"
                        # Anmerkungen anzeigen, wenn vorhanden
                        if 'customOrder' in row and row['customOrder']:
                            formatted_row['Details'] = f"Anmerkung: {row['customOrder']}"
                        else:
                            formatted_row['Details'] = ''
                    elif product == 'Bäcker':
                        baecker_item = row.get('baeckerItem', '-')
                        formatted_row['Bestellung'] = f"Bäcker"
                        formatted_row['Details'] = f"{baecker_item}"
                    else:
                        sauce = row.get('sauce', 'keine')
                        formatted_row['Bestellung'] = f"{product}"
                        details = [f"Sauce: {sauce}"]
                        # Anmerkungen anzeigen, wenn vorhanden
                        if 'customOrder' in row and row['customOrder']:
                            details.append(f"Anmerkung: {row['customOrder']}")
                        formatted_row['Details'] = ", ".join(details)
                
                else:
                    formatted_row['Restaurant'] = order_type.capitalize()
                    formatted_row['Bestellung'] = '-'
                    formatted_row['Details'] = '-'
                
                formatted_rows.append(formatted_row)
            
            return pd.DataFrame(formatted_rows)
        
        return pd.DataFrame()