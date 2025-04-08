#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility functions for the LunchSquad application
"""

import streamlit as st
import pandas as pd
import json
import base64
import io
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def format_order_item(order):
    """Format an order as a readable string"""
    order_type = order.get("type", "")

    if order_type == "yamyam":
        return f"{order['name']} - YamYam Nr. {order['number']}"

    elif order_type == "doner":
        shop = order.get("shop", "")
        product = order.get("product", "")
        sauces = ", ".join(order.get("sauces", [])) or "keine"
        
        # Verarbeitung der Extras mit Freitextfeld
        extras_list = []
        for extra in order.get("extras", []):
            if extra.startswith("custom:"):
                # Freitexteintrag extrahieren
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
        
        extras = ", ".join(extras_list) or "keine"

        # Map values to display names
        shop_map = {
            "bruder": "Döner Bruder",
            "king": "King Kebabo's",
            "aldi": "Aldi Döner"
        }
        
        product_map = {
            "doner": "Döner",
            "durum": "Dürüm",
            "falafel-doner": "Falafel-Döner",
            "falafel-durum": "Falafel-Dürüm",
            "box": "Dönerbox"
        }
        
        shop_display = shop_map.get(shop, shop)
        product_display = product_map.get(product, product)

        result = f"{order['name']} - {shop_display} - {product_display}"

        if product == "box":
            box_type = order.get("boxType", "")
            box_map = {"pommes": "mit Pommes", "salat": "mit Salat"}
            box_display = box_map.get(box_type, box_type)
            result += f" ({box_display})"

        result += f" | Soßen: {sauces}"
        if extras != "keine":
            result += f" | Extras: {extras}"

        return result

    elif order_type == "edeka":
        product = order.get("product", "")

        if product == "Salat":
            salat_type = order.get("salatType", "")
            return f"{order['name']} - {salat_type} Salat"
        elif product == "Bäcker":
            baecker_item = order.get("baeckerItem", "")
            return f"{order['name']} - Bäcker: {baecker_item}"
        else:
            sauce = order.get("sauce", "keine")
            return f"{order['name']} - {product} mit {sauce}"

    return f"{order['name']} - Unbekannte Bestellung"

def create_download_link(df, filename="orders.csv", text="Download CSV"):
    """
    Create a download link for a DataFrame as CSV
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'data:file/csv;base64,{b64}'
    return href

def create_download_link_json(data, filename="orders.json", text="Download JSON"):
    """
    Create a download link for data as JSON
    """
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    b64 = base64.b64encode(json_str.encode('utf-8')).decode()
    href = f'data:file/json;base64,{b64}'
    return href

def create_text_report(orders):
    """
    Create a text report of orders for downloading
    """
    report = f"LunchSquad Bestellungen - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    report += "=" * 50 + "\n\n"
    
    if not orders:
        report += "Keine Bestellungen vorhanden.\n"
        return report
    
    for i, order in enumerate(orders, 1):
        report += f"{i}. {format_order_item(order)}\n"
    
    return report

def create_download_link_text(text_content, filename="orders.txt", link_text="Download TXT"):
    """
    Create a download link for text content
    """
    b64 = base64.b64encode(text_content.encode('utf-8')).decode()
    href = f'data:file/txt;base64,{b64}'
    return href

def create_image_report(orders):
    """
    Create an image report of orders
    Returns a PIL Image object
    """
    if not orders:
        return None
    
    # Create a blank image
    width = 800
    height = 100 + (len(orders) * 30)  # Adjust height based on number of orders
    img = Image.new('RGB', (width, height), color=(30, 41, 59))  # Dark background
    
    try:
        draw = ImageDraw.Draw(img)
        
        # Try to load a font or use default
        try:
            # Use a web-safe font that's likely available
            font = ImageFont.truetype("Arial", 12)
            title_font = ImageFont.truetype("Arial", 16)
        except:
            font = ImageFont.load_default()
            title_font = font
        
        # Draw title
        titel = f"LunchSquad - Bestellungen vom {datetime.now().strftime('%Y-%m-%d')}"
        draw.text((20, 20), titel, fill=(248, 250, 252), font=title_font)
        draw.line([(20, 50), (width - 20, 50)], fill=(203, 213, 225), width=2)
        
        # Draw each order
        y_pos = 70
        for i, order in enumerate(orders, 1):
            order_text = f"{i}. {format_order_item(order)}"
            # Wrap text if it's too long
            if len(order_text) > 80:
                order_text = order_text[:77] + "..."
            draw.text((30, y_pos), order_text, fill=(248, 250, 252), font=font)
            y_pos += 25
            
            # Draw a separator line
            if i < len(orders):
                draw.line([(30, y_pos - 5), (width - 30, y_pos - 5)], fill=(71, 85, 105), width=1)
        
        return img
    
    except Exception as e:
        st.error(f"Error creating image report: {e}")
        return None

def create_download_link_image(img, filename="orders.png", link_text="Download PNG"):
    """
    Create a download link for an image
    """
    if img is None:
        return None
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    href = f'data:image/png;base64,{b64}'
    return href

def format_timestamp(timestamp):
    """Format an ISO timestamp into a readable format"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%d.%m.%Y %H:%M")
    except (ValueError, TypeError):
        return "Unbekannt"

def validate_yamyam_order(order):
    """Validate YamYam order specifics"""
    if not order.get("name"):
        return False, "Bitte einen Namen eingeben."
        
    if not order.get("number"):
        return False, "Bitte eine Nummer eingeben."
    
    try:
        number = int(order["number"])
        if not (1 <= number <= 73):
            return False, "Die Nummer muss zwischen 1 und 73 liegen."
    except ValueError:
        return False, "Die Nummer muss eine ganze Zahl sein."
    
    return True, ""

def validate_doner_order(order):
    """Validate Döner order specifics"""
    if not order.get("name"):
        return False, "Bitte einen Namen eingeben."
        
    if not order.get("shop"):
        return False, "Bitte einen Laden auswählen."
        
    if not order.get("product"):
        return False, "Bitte ein Produkt auswählen."
    
    if len(order.get("sauces", [])) > 2:
        return False, "Maximal 2 Soßen erlaubt."
        
    if len(order.get("extras", [])) > 3:
        return False, "Maximal 3 Extras erlaubt."
    
    return True, ""

def validate_edeka_order(order):
    """Validate Edeka order specifics"""
    if not order.get("name"):
        return False, "Bitte einen Namen eingeben."
        
    if not order.get("product"):
        return False, "Bitte ein Produkt auswählen."
    
    # Product-specific validation
    if order["product"] == "Salat" and not order.get("salatType"):
        return False, "Bitte eine Salatsorte auswählen."
    
    if order["product"] == "Bäcker" and not order.get("baeckerItem"):
        return False, "Bitte eine Bestellung für den Bäcker eingeben."
    
    if order["product"] != "Salat" and order["product"] != "Bäcker" and not order.get("sauce"):
        return False, "Bitte eine Sauce auswählen."
    
    return True, ""
