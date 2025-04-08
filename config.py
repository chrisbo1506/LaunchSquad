#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration settings for the LunchSquad app
"""

# General app settings
APP_TITLE = "LunchSquad"
DEFAULT_ORDER_FILE = "lunch_orders.json"

# YamYam options
YAMYAM_OPTIONS = {
    "name": "YamYam",
    "icon": "🍚",
    "description": "Koreanisches Restaurant mit verschiedenen Bowl-Optionen",
    "max_number": 100  # Maximum menu item number
}

# Döner options
DONER_OPTIONS = {
    "name": "Döner",
    "icon": "🥙",
    "description": "Verschiedene Döner-Shops in der Nähe",
    
    # Shops
    "shops": ["Döner Bruder", "King Kebabo's", "Aldi Döner"],
    "shop_values": ["bruder", "king", "aldi"],
    
    # Products
    "products": ["Döner", "Dürüm", "Falafel-Döner", "Falafel-Dürüm", "Dönerbox"],
    "product_values": ["doner", "durum", "falafel-doner", "falafel-durum", "box"],
    
    # Box options
    "box_types": ["mit Pommes", "mit Salat"],
    "box_values": ["pommes", "salat"],
    
    # Sauces
    "sauces": ["Kräuter", "Knoblauch", "Scharf", "Cocktail", "Chili Mango"],
    "sauce_values": ["kraeuter", "knoblauch", "scharf", "cocktail", "Chili Mango"],
    
    # Spice levels
    "spice_levels": ["Nicht scharf", "Normal scharf", "Extra scharf"],
    "spice_values": ["none", "normal", "extra"],
    
    # Extras (things to leave out)
    "extras": ["Ohne Zwiebel", "Ohne Tomate", "Ohne Blaukraut", "Ohne Salat", 
               "Ohne Soße", "Ohne Grillgemüse", "Ohne Gurke"],
    "extra_values": ["ohne-zwiebel", "ohne-tomate", "ohne-blaukraut", "ohne-salat",
                    "ohne-sosse", "ohne-grillgemuese", "ohne-gurke"]
}

# Edeka options
EDEKA_OPTIONS = {
    "name": "Edeka",
    "icon": "🛒",
    "description": "Snacks und Supermarkt-Essen",
    
    # Products
    "products": ["Salat", "Sandwich", "Wrap", "Bäcker"],
    
    # Salad options
    "salads": ["Kleiner Salat", "Großer Salat", "Spezial Salat"],
    
    # Sandwich/Wrap sauces
    "sauces": ["Mayo", "Senf", "Ketchup", "BBQ", "Süß-Sauer", "Ohne Sauce"]
}
