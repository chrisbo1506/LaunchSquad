#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration settings for the LunchSquad app
"""

# App info
APP_TITLE = "LunchSquad - Team Lunch Organizer"
APP_VERSION = "1.0.0"

# Color scheme (dark theme)
COLORS = {
    "primary": "#3b82f6",      # Blue
    "secondary": "#6366f1",    # Indigo
    "accent": "#8b5cf6",       # Violet
    "red": "#e11d48",          # Red for warnings/danger
    "green": "#22c55e",        # Green for success
    "bg_dark": "#1e293b",      # Dark background
    "bg_medium": "#334155",    # Medium background
    "bg_light": "#475569",     # Light background
    "text_light": "#f8fafc",   # Light text for dark backgrounds
    "text_medium": "#cbd5e1",  # Medium text
    "text_dark": "#1e293b",    # Dark text for light backgrounds
    "input_bg": "#e2e8f0",     # Input background
    "link": "#38bdf8",         # Link color
}

# Font styles (Not directly used in Streamlit, but kept for reference)
FONT_STYLES = {
    "title": ("Helvetica", 22, "bold"),
    "subtitle": ("Helvetica", 16, "bold"),
    "section_title": ("Helvetica", 14, "bold"),
    "normal": ("Helvetica", 12),
    "small": ("Helvetica", 10),
    "button": ("Helvetica", 12, "bold"),
    "link": ("Helvetica", 10, "underline"),
}

# Restaurant options
YAMYAM_OPTIONS = {
    "name": "YamYam",
    "description": "Asiatische Küche",
    "icon": "🍜",
    "max_number": 73
}

DONER_OPTIONS = {
    "name": "Döner",
    "description": "Türkische Spezialitäten",
    "icon": "🥙",
    "shops": ["Döner Bruder", "King Kebabo's", "Aldi Döner"],
    "shop_values": ["bruder", "king", "aldi"],
    "products": ["Döner", "Dürüm", "Falafel-Döner", "Falafel-Dürüm", "Dönerbox"],
    "product_values": ["doner", "durum", "falafel-doner", "falafel-durum", "box"],
    "sauces": ["Knoblauch", "Jogurt", "Cocktail"],
    "sauce_values": ["knoblauch", "jogurt", "cocktail"],
    "extras": ["Ohne Zwiebel", "Ohne Tomate", "Ohne Blaukraut", "Ohne Salat", "Ohne Soße", "Ohne Grillgemüse", "Ohne Gurke"],
    "extra_values": ["ohne-zwiebel", "ohne-tomate", "ohne-blaukraut", "ohne-salat", "ohne-sosse", "ohne-grillgemuese", "ohne-gurke"],
    "spice_levels": ["Nicht scharf", "Normal", "Sehr scharf"],
    "spice_values": ["none", "normal", "extra"],
    "box_types": ["Mit Pommes", "Mit Salat"],
    "box_values": ["pommes", "salat"]
}

EDEKA_OPTIONS = {
    "name": "Edeka",
    "description": "Belegte Brötchen & Salate",
    "icon": "🍞",
    "products": ["Leberkässemmel", "Bratensemmel", "Schnitzelsemmel", "Salat", "Bäcker"],
    "salads": ["Greek Salat", "Hühnchen Salat", "Vegetarischer Salat", "Käse Salat", "Asia Salat"],
    "sauces": ["Ketchup", "Mayonnaise", "Senf", "Remoulade", "Curry Sauce"]
}

# File settings
DEFAULT_ORDER_FILE = "lunch_orders.json"
