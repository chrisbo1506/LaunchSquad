#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility functions for the LunchSquad application
"""

import base64
import streamlit as st
import pandas as pd
import io
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def format_order_item(order):
    """Format an order as a readable string"""
    name = order.get("name", "")
    order_type = order.get("type", "")
    timestamp = order.get("timestamp", "")
    
    formatted_time = ""
    if timestamp:
        try:
            dt = datetime.fromisoformat(timestamp)
            formatted_time = dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            pass
    
    if order_type == "yamyam":
        return f"{formatted_time} - {name}: YamYam #{order.get('number', '')}"
    
    elif order_type == "doner":
        product_map = {
            "doner": "Döner",
            "durum": "Dürüm",
            "falafel-doner": "Falafel-Döner",
            "falafel-durum": "Falafel-Dürüm",
            "box": "Dönerbox"
        }
        
        shop_map = {
            "bruder": "Döner Bruder",
            "king": "King Kebabo's",
            "aldi": "Aldi Döner"
        }
        
        product = product_map.get(order.get("product", ""), order.get("product", ""))
        shop = shop_map.get(order.get("shop", ""), order.get("shop", ""))
        
        box_type = ""
        if order.get("product") == "box" and "boxType" in order:
            box_map = {"pommes": "mit Pommes", "salat": "mit Salat"}
            box_type = f" ({box_map.get(order['boxType'], order['boxType'])})"
        
        return f"{formatted_time} - {name}: {product}{box_type} ({shop})"
    
    elif order_type == "edeka":
        product = order.get("product", "")
        if product == "Salat":
            return f"{formatted_time} - {name}: Edeka Salatbar - {order.get('salatType', '')}"
        elif product == "Bäcker":
            return f"{formatted_time} - {name}: Edeka Bäcker - {order.get('baeckerItem', '')}"
        else:
            return f"{formatted_time} - {name}: Edeka {product} - Sauce: {order.get('sauce', 'keine')}"
    
    else:
        return f"{formatted_time} - {name}: Unknown order type: {order_type}"

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
    import json
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'data:file/json;base64,{b64}'
    return href

def create_text_report(orders):
    """
    Create a text report of orders for downloading
    """
    if not orders:
        return "No orders available."
    
    text = "LunchSquad - Team Lunch Orders\n"
    text += "=" * 40 + "\n\n"
    text += f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Group by restaurant type
    yamyam_orders = [o for o in orders if o.get("type") == "yamyam"]
    doner_orders = [o for o in orders if o.get("type") == "doner"]
    edeka_orders = [o for o in orders if o.get("type") == "edeka"]
    
    # YamYam orders
    if yamyam_orders:
        text += "YamYam Orders:\n"
        text += "-" * 20 + "\n"
        for order in yamyam_orders:
            text += f"- {order.get('name', '')}: #{order.get('number', '')}\n"
        text += "\n"
    
    # Döner orders
    if doner_orders:
        text += "Döner Orders:\n"
        text += "-" * 20 + "\n"
        for order in doner_orders:
            product_map = {
                "doner": "Döner",
                "durum": "Dürüm",
                "falafel-doner": "Falafel-Döner",
                "falafel-durum": "Falafel-Dürüm",
                "box": "Dönerbox"
            }
            shop_map = {
                "bruder": "Döner Bruder",
                "king": "King Kebabo's",
                "aldi": "Aldi Döner"
            }
            product = product_map.get(order.get("product", ""), order.get("product", ""))
            shop = shop_map.get(order.get("shop", ""), order.get("shop", ""))
            sauces = ", ".join(order.get("sauces", [])) or "keine"
            spice_map = {"none": "nicht scharf", "normal": "normal scharf", "extra": "sehr scharf"}
            spice = spice_map.get(order.get("spiceLevel", ""), order.get("spiceLevel", ""))
            
            extras = []
            for extra in order.get("extras", []):
                if isinstance(extra, str) and extra.startswith("custom:"):
                    extras.append(extra[7:])  # Remove "custom:" prefix
                else:
                    extras.append(extra)
            extras_str = ", ".join(extras) or "keine"
            
            box_type = ""
            if order.get("product") == "box" and "boxType" in order:
                box_map = {"pommes": "mit Pommes", "salat": "mit Salat"}
                box_type = f" ({box_map.get(order['boxType'], order['boxType'])})"
            
            text += f"- {order.get('name', '')}: {product}{box_type} ({shop})\n"
            text += f"  Soßen: {sauces}\n"
            text += f"  Extras: {extras_str}\n"
            text += f"  Schärfe: {spice}\n\n"
    
    # Edeka orders
    if edeka_orders:
        text += "Edeka Orders:\n"
        text += "-" * 20 + "\n"
        for order in edeka_orders:
            product = order.get("product", "")
            if product == "Salat":
                text += f"- {order.get('name', '')}: Salatbar - {order.get('salatType', '')}\n"
            elif product == "Bäcker":
                text += f"- {order.get('name', '')}: Bäcker - {order.get('baeckerItem', '')}\n"
            else:
                text += f"- {order.get('name', '')}: {product} - Sauce: {order.get('sauce', 'keine')}\n"
        text += "\n"
    
    text += "=" * 40 + "\n"
    text += "Enjoy your meal! | LunchSquad - Team Lunch Organizer"
    
    return text

def create_download_link_text(text_content, filename="orders.txt", link_text="Download TXT"):
    """
    Create a download link for text content
    """
    b64 = base64.b64encode(text_content.encode()).decode()
    href = f'data:file/txt;base64,{b64}'
    return href

def create_image_report(orders):
    """
    Create an image report of orders
    Returns a PIL Image object
    """
    if not orders:
        return None
    
    # Create an image
    width, height = 1000, max(600, 180 + 60 * len(orders))
    img = Image.new('RGB', (width, height), color=(40, 40, 40))
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to load a font (fallback to default if not available)
        try:
            # For Linux servers
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
            header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
            text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except OSError:
            try:
                # For Windows
                title_font = ImageFont.truetype("arial.ttf", 28)
                header_font = ImageFont.truetype("arial.ttf", 20)
                text_font = ImageFont.truetype("arial.ttf", 16)
            except OSError:
                # Fallback
                title_font = ImageFont.load_default()
                header_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
        
        # Draw title
        draw.text((50, 40), "LunchSquad - Team Lunch Orders", fill=(255, 255, 255), font=title_font)
        draw.text((50, 80), f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fill=(180, 180, 180), font=text_font)
        draw.line([(50, 120), (width-50, 120)], fill=(100, 100, 100), width=2)
        
        # Group by restaurant type
        yamyam_orders = [o for o in orders if o.get("type") == "yamyam"]
        doner_orders = [o for o in orders if o.get("type") == "doner"]
        edeka_orders = [o for o in orders if o.get("type") == "edeka"]
        
        y_pos = 140
        
        # YamYam orders
        if yamyam_orders:
            draw.text((50, y_pos), "YamYam Orders:", fill=(255, 220, 100), font=header_font)
            y_pos += 30
            for order in yamyam_orders:
                draw.text((70, y_pos), f"{order.get('name', '')}: #{order.get('number', '')}", 
                         fill=(255, 255, 255), font=text_font)
                y_pos += 25
            y_pos += 20
        
        # Döner orders
        if doner_orders:
            draw.text((50, y_pos), "Döner Orders:", fill=(255, 220, 100), font=header_font)
            y_pos += 30
            for order in doner_orders:
                product_map = {
                    "doner": "Döner",
                    "durum": "Dürüm",
                    "falafel-doner": "Falafel-Döner",
                    "falafel-durum": "Falafel-Dürüm",
                    "box": "Dönerbox"
                }
                shop_map = {
                    "bruder": "Döner Bruder",
                    "king": "King Kebabo's",
                    "aldi": "Aldi Döner"
                }
                product = product_map.get(order.get("product", ""), order.get("product", ""))
                shop = shop_map.get(order.get("shop", ""), order.get("shop", ""))
                
                box_type = ""
                if order.get("product") == "box" and "boxType" in order:
                    box_map = {"pommes": "mit Pommes", "salat": "mit Salat"}
                    box_type = f" ({box_map.get(order['boxType'], order['boxType'])})"
                
                draw.text((70, y_pos), f"{order.get('name', '')}: {product}{box_type} ({shop})", 
                         fill=(255, 255, 255), font=text_font)
                y_pos += 25
                
                sauces = ", ".join(order.get("sauces", [])) or "keine"
                draw.text((90, y_pos), f"Soßen: {sauces}", fill=(200, 200, 200), font=text_font)
                y_pos += 25
                
                extras = []
                for extra in order.get("extras", []):
                    if isinstance(extra, str) and extra.startswith("custom:"):
                        extras.append(extra[7:])  # Remove "custom:" prefix
                    else:
                        extras.append(extra)
                extras_str = ", ".join(extras) or "keine"
                draw.text((90, y_pos), f"Extras: {extras_str}", fill=(200, 200, 200), font=text_font)
                y_pos += 25
                
                spice_map = {"none": "nicht scharf", "normal": "normal scharf", "extra": "sehr scharf"}
                spice = spice_map.get(order.get("spiceLevel", ""), order.get("spiceLevel", ""))
                draw.text((90, y_pos), f"Schärfe: {spice}", fill=(200, 200, 200), font=text_font)
                y_pos += 40
        
        # Edeka orders
        if edeka_orders:
            draw.text((50, y_pos), "Edeka Orders:", fill=(255, 220, 100), font=header_font)
            y_pos += 30
            for order in edeka_orders:
                product = order.get("product", "")
                if product == "Salat":
                    draw.text((70, y_pos), f"{order.get('name', '')}: Salatbar - {order.get('salatType', '')}", 
                             fill=(255, 255, 255), font=text_font)
                elif product == "Bäcker":
                    draw.text((70, y_pos), f"{order.get('name', '')}: Bäcker - {order.get('baeckerItem', '')}", 
                             fill=(255, 255, 255), font=text_font)
                else:
                    draw.text((70, y_pos), f"{order.get('name', '')}: {product} - Sauce: {order.get('sauce', 'keine')}", 
                             fill=(255, 255, 255), font=text_font)
                y_pos += 25
        
        # Footer
        draw.line([(50, height-60), (width-50, height-60)], fill=(100, 100, 100), width=2)
        draw.text((50, height-40), "Enjoy your meal! | LunchSquad - Team Lunch Organizer", 
                 fill=(180, 180, 180), font=text_font)
        
        return img
        
    except Exception as e:
        print(f"Error creating image: {e}")
        return None

def create_download_link_image(img, filename="orders.png", link_text="Download PNG"):
    """
    Create a download link for an image
    """
    try:
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode()
        href = f'data:image/png;base64,{b64}'
        return href
    except Exception as e:
        print(f"Error creating image download link: {e}")
        return ""

def format_timestamp(timestamp):
    """Format an ISO timestamp into a readable format"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        return str(timestamp)

def validate_yamyam_order(order):
    """Validate YamYam order specifics"""
    name = order.get("name", "").strip()
    number = order.get("number", "").strip()
    
    if not name:
        return (False, "Bitte gib deinen Namen ein.")
    
    if not number:
        return (False, "Bitte gib eine Nummer ein.")
    
    try:
        num = int(number)
        if num < 1 or num > 100:  # Assuming max 100 items on menu
            return (False, "Bitte gib eine gültige Nummer ein (1-100).")
    except ValueError:
        return (False, "Bitte gib eine gültige Nummer ein.")
    
    return (True, "")

def validate_doner_order(order):
    """Validate Döner order specifics"""
    name = order.get("name", "").strip()
    shop = order.get("shop", "")
    product = order.get("product", "")
    sauces = order.get("sauces", [])
    
    if not name:
        return (False, "Bitte gib deinen Namen ein.")
    
    if not shop:
        return (False, "Bitte wähle einen Laden aus.")
    
    if not product:
        return (False, "Bitte wähle ein Produkt aus.")
    
    if product == "box" and "boxType" not in order:
        return (False, "Bitte wähle einen Box-Typ aus.")
    
    if len(sauces) > 2:
        return (False, "Bitte wähle maximal 2 Soßen aus.")
    
    extras = [e for e in order.get("extras", []) if not (isinstance(e, str) and e.startswith("custom:"))]
    if len(extras) > 3:
        return (False, "Bitte wähle maximal 3 Standard-Extras aus.")
    
    return (True, "")

def validate_edeka_order(order):
    """Validate Edeka order specifics"""
    name = order.get("name", "").strip()
    product = order.get("product", "")
    
    if not name:
        return (False, "Bitte gib deinen Namen ein.")
    
    if not product:
        return (False, "Bitte wähle ein Produkt aus.")
    
    if product == "Salat" and not order.get("salatType"):
        return (False, "Bitte wähle eine Salat-Option aus.")
    
    if product == "Bäcker" and not order.get("baeckerItem", "").strip():
        return (False, "Bitte gib an, was du vom Bäcker möchtest.")
    
    return (True, "")
