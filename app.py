#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LunchSquad - Team Lunch Organizer (Streamlit version)

A web application to organize lunch orders for a team, supporting multiple
restaurants (YamYam, Döner, Edeka) with customizable orders.
"""

import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import webbrowser
from PIL import Image

from models import OrderManager
from config import (
    APP_TITLE, 
    YAMYAM_OPTIONS, 
    DONER_OPTIONS, 
    EDEKA_OPTIONS, 
    DEFAULT_ORDER_FILE
)
from utils import (
    create_download_link,
    create_download_link_json,
    create_download_link_text,
    create_text_report,
    create_image_report,
    create_download_link_image,
    validate_yamyam_order,
    validate_doner_order,
    validate_edeka_order
)

# Set page config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🍱",
    layout="wide"
)

# Initialize session state
if "orders" not in st.session_state:
    st.session_state.orders = []
if "current_view" not in st.session_state:
    st.session_state.current_view = "main"
if "selected_shop" not in st.session_state:
    st.session_state.selected_shop = None
# Initialize orders_data if not already present
if "orders_data" not in st.session_state:
    st.session_state.orders_data = []

if "order_manager" not in st.session_state:
    # Initialize order manager and load orders
    st.session_state.order_manager = OrderManager()
    # Copy orders into session state for UI management
    st.session_state.orders = st.session_state.order_manager.get_orders()

def save_orders():
    """Save orders to JSON file"""
    # Sicherstellen, dass OrderManager die aktuelle Liste hat
    st.session_state.order_manager.orders = st.session_state.orders
    # Jetzt speichern
    success = st.session_state.order_manager.save_orders()
    if success:
        st.success("Bestellungen wurden erfolgreich gespeichert.")
    else:
        st.error("Bestellungen konnten nicht gespeichert werden.")

def add_order(order_data):
    """Add a new order"""
    # Add order to session state
    order_data["timestamp"] = datetime.now().isoformat()
    st.session_state.orders.append(order_data)
    # Update order manager
    st.session_state.order_manager.orders = st.session_state.orders
    # Save orders explicitly
    st.session_state.order_manager.save_orders()
    
    # Inform user
    st.success(f"Bestellung für {order_data['name']} hinzugefügt!")
    
    # Return to main view
    st.session_state.current_view = "order_list"
    st.rerun()

def remove_order(index):
    """Remove an order by index"""
    if 0 <= index < len(st.session_state.orders):
        del st.session_state.orders[index]
        # Update order manager
        st.session_state.order_manager.orders = st.session_state.orders
        # Save orders explicitly
        st.session_state.order_manager.save_orders()
        st.success("Bestellung entfernt.")
        st.rerun()

def clear_orders():
    """Clear all orders"""
    # Clear session state orders
    st.session_state.orders = []
    # Update the order manager with empty list
    st.session_state.order_manager.orders = []
    # Call the clear_orders method which should also save the empty list
    success = st.session_state.order_manager.clear_orders()
    if success:
        st.success("Alle Bestellungen wurden gelöscht.")
    else:
        st.error("Fehler beim Löschen der Bestellungen.")
    st.rerun()

def change_view(view_name):
    """Change the current view"""
    st.session_state.current_view = view_name
    st.rerun()

def select_shop(shop_value):
    """Select a specific döner shop"""
    st.session_state.selected_shop = shop_value

# App Title
st.title(APP_TITLE)

# Sidebar
with st.sidebar:
    st.title("Menü")
    
    if st.button("Restaurantauswahl", use_container_width=True):
        change_view("main")
    
    if st.button("Bestellungen anzeigen", use_container_width=True):
        change_view("order_list")
    
    st.divider()
    
    if st.button("Speichern", use_container_width=True):
        save_orders()
    
    if st.button("Alle Bestellungen löschen", use_container_width=True):
        # Confirmation for dangerous operation
        confirmation = st.sidebar.checkbox("Bestätigen: Alle Bestellungen unwiderruflich löschen?")
        if confirmation:
            clear_orders()

# Main Content
if st.session_state.current_view == "main":
    st.header("Restaurant wählen")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("YamYam")
        st.write("Koreanisches Restaurant mit verschiedenen Bowl-Optionen")
        if st.button("YamYam auswählen", key="select_yamyam"):
            change_view("yamyam")
    
    with col2:
        st.subheader("Döner")
        st.write("Verschiedene Döner-Shops in der Nähe")
        if st.button("Döner auswählen", key="select_doner"):
            change_view("doner_shop")
    
    with col3:
        st.subheader("Edeka")
        st.write("Snacks und Supermarkt-Essen")
        if st.button("Edeka auswählen", key="select_edeka"):
            change_view("edeka")

elif st.session_state.current_view == "yamyam":
    st.header("YamYam Bestellung")
    
    with st.form("yamyam_form"):
        name = st.text_input("Name", placeholder="Dein Name")
        
        # YamYam specific options
        option_number = st.selectbox("Welche Nummer?", options=YAMYAM_OPTIONS)
        
        # Submit form
        submitted = st.form_submit_button("Bestellung hinzufügen")
        
        if submitted:
            if not name:
                st.error("Bitte gib deinen Namen ein!")
            else:
                order = {
                    "type": "yamyam",
                    "name": name,
                    "number": option_number,
                }
                
                # Validate order
                validation_result = validate_yamyam_order(order)
                if validation_result["valid"]:
                    add_order(order)
                else:
                    st.error(validation_result["message"])
    
    if st.button("Zurück zur Restaurantauswahl"):
        change_view("main")

elif st.session_state.current_view == "doner_shop":
    st.header("Döner Shop auswählen")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Döner Bruder")
        st.write("Der Klassiker an der Ecke")
        if st.button("Döner Bruder auswählen"):
            select_shop("bruder")
            change_view("doner")
    
    with col2:
        st.subheader("King Kebabo's")
        st.write("Premium Döner mit vielen Extras")
        if st.button("King Kebabo's auswählen"):
            select_shop("king")
            change_view("doner")
    
    with col3:
        st.subheader("Aldi Döner")
        st.write("Günstig und gut")
        if st.button("Aldi Döner auswählen"):
            select_shop("aldi")
            change_view("doner")
    
    if st.button("Zurück zur Restaurantauswahl", key="doner_shop_back"):
        change_view("main")

elif st.session_state.current_view == "doner":
    shop_names = {
        "bruder": "Döner Bruder",
        "king": "King Kebabo's",
        "aldi": "Aldi Döner"
    }
    
    shop_name = shop_names.get(st.session_state.selected_shop, "Döner Shop")
    st.header(f"{shop_name} Bestellung")
    
    with st.form("doner_form"):
        name = st.text_input("Name", placeholder="Dein Name")
        
        # Döner specific options
        product = st.selectbox(
            "Produkt",
            options=DONER_OPTIONS["products"].keys(),
            format_func=lambda x: DONER_OPTIONS["products"][x]
        )
        
        # Box type for Dönerbox
        box_type = None
        if product == "box":
            box_type = st.radio(
                "Box-Typ",
                options=["pommes", "salat"],
                format_func=lambda x: "mit Pommes" if x == "pommes" else "mit Salat"
            )
        
        # Sauces
        st.write("Soßen")
        sauces = []
        sauce_cols = st.columns(3)
        for i, sauce in enumerate(DONER_OPTIONS["sauces"]):
            col_idx = i % 3
            with sauce_cols[col_idx]:
                if st.checkbox(sauce, key=f"sauce_{sauce}"):
                    sauces.append(sauce)
        
        # Extras
        st.write("Extras")
        extras = []
        extras_cols = st.columns(3)
        for i, extra in enumerate(DONER_OPTIONS["extras"]):
            col_idx = i % 3
            with extras_cols[col_idx]:
                if st.checkbox(extra, key=f"extra_{extra}"):
                    extras.append(extra)
        
        # Custom extras (free text)
        custom_extras = st.text_input("Weitere individuelle Wünsche", placeholder="z.B. Extra scharf, ohne Salat, etc.")
        
        # Spice level
        spice_level = st.radio(
            "Schärfegrad",
            options=["none", "normal", "extra"],
            format_func=lambda x: {
                "none": "Nicht scharf",
                "normal": "Normal scharf",
                "extra": "Extra scharf"
            }[x]
        )
        
        # Submit form
        submitted = st.form_submit_button("Bestellung hinzufügen")
        
        if submitted:
            if not name:
                st.error("Bitte gib deinen Namen ein!")
            else:
                order = {
                    "type": "doner",
                    "name": name,
                    "shop": st.session_state.selected_shop,
                    "product": product,
                    "sauces": sauces,
                    "extras": extras,
                    "spiceLevel": spice_level
                }
                
                # Add box type if it's a box
                if product == "box" and box_type:
                    order["boxType"] = box_type
                
                # Add custom extras if provided
                if custom_extras:
                    # Add custom extras with a prefix to distinguish them
                    order["extras"].append(f"custom:{custom_extras}")
                
                # Validate order
                validation_result = validate_doner_order(order)
                if validation_result["valid"]:
                    add_order(order)
                else:
                    st.error(validation_result["message"])
    
    if st.button("Andere Döner Shop auswählen"):
        change_view("doner_shop")
    
    if st.button("Zurück zur Restaurantauswahl", key="doner_back"):
        change_view("main")

elif st.session_state.current_view == "edeka":
    st.header("Edeka Bestellung")
    
    with st.form("edeka_form"):
        name = st.text_input("Name", placeholder="Dein Name")
        
        # Edeka specific options
        product_type = st.selectbox(
            "Was möchtest du bestellen?", 
            options=list(EDEKA_OPTIONS.keys()),
            format_func=lambda x: EDEKA_OPTIONS[x]["name"]
        )
        
        # Product-specific options
        if product_type == "Salat":
            salat_type = st.selectbox(
                "Welche Salatbar-Option?",
                options=EDEKA_OPTIONS["Salat"]["options"]
            )
        elif product_type == "Sandwich":
            sauce = st.selectbox(
                "Welche Sauce?",
                options=EDEKA_OPTIONS["Sandwich"]["sauces"],
                index=0
            )
        elif product_type == "Bäcker":
            baecker_item = st.text_input(
                "Was vom Bäcker?",
                placeholder="z.B. Laugenbrezel, Käsebrötchen, etc."
            )
        
        # Submit form
        submitted = st.form_submit_button("Bestellung hinzufügen")
        
        if submitted:
            if not name:
                st.error("Bitte gib deinen Namen ein!")
            else:
                order = {
                    "type": "edeka",
                    "name": name,
                    "product": product_type
                }
                
                # Add product-specific details
                if product_type == "Salat":
                    order["salatType"] = salat_type
                elif product_type == "Sandwich":
                    order["sauce"] = sauce
                elif product_type == "Bäcker":
                    if not baecker_item:
                        st.error("Bitte gib an, was du vom Bäcker möchtest!")
                        st.stop()
                    order["baeckerItem"] = baecker_item
                
                # Validate order
                validation_result = validate_edeka_order(order)
                if validation_result["valid"]:
                    add_order(order)
                else:
                    st.error(validation_result["message"])
    
    if st.button("Zurück zur Restaurantauswahl", key="edeka_back"):
        change_view("main")

elif st.session_state.current_view == "order_list":
    st.header("Bestellungen")
    
    orders = st.session_state.orders
    
    if not orders:
        st.info("Noch keine Bestellungen vorhanden.")
    else:
        # Create a DataFrame for display
        df = st.session_state.order_manager.get_orders_dataframe()
        
        # Filter options
        with st.expander("Filter und Sortierung"):
            # Restaurant type filter
            st.write("Nach Restaurant filtern:")
            filter_cols = st.columns(3)
            with filter_cols[0]:
                show_yamyam = st.checkbox("YamYam", value=True)
            with filter_cols[1]:
                show_doner = st.checkbox("Döner", value=True)
            with filter_cols[2]:
                show_edeka = st.checkbox("Edeka", value=True)
            
            # Apply filters
            mask = pd.Series(True, index=df.index)
            if not show_yamyam:
                mask = mask & (df["Restaurant"] != "YamYam")
            if not show_doner:
                mask = mask & (df["Restaurant"] != "Döner")
            if not show_edeka:
                mask = mask & (df["Restaurant"] != "Edeka")
            
            df_filtered = df[mask]
            
            # Sorting
            st.write("Sortieren nach:")
            sort_cols = st.columns(3)
            with sort_cols[0]:
                sort_by_time = st.checkbox("Zeitpunkt", value=True)
            with sort_cols[1]:
                sort_by_name = st.checkbox("Name")
            with sort_cols[2]:
                sort_by_restaurant = st.checkbox("Restaurant")
            
            # Apply sorting
            if sort_by_time:
                df_filtered = df_filtered.sort_values("Zeitpunkt")
            if sort_by_name:
                df_filtered = df_filtered.sort_values("Name")
            if sort_by_restaurant:
                df_filtered = df_filtered.sort_values("Restaurant")
        
        # Display the filtered/sorted DataFrame
        st.dataframe(
            df_filtered,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Zeitpunkt": st.column_config.DatetimeColumn(
                    "Zeitpunkt",
                    format="DD.MM.YYYY, HH:mm"
                )
            }
        )
        
        # Export options
        with st.expander("Export-Optionen"):
            export_cols = st.columns(4)
            with export_cols[0]:
                # Download as CSV
                st.download_button(
                    "CSV herunterladen",
                    data=df_filtered.to_csv(index=False),
                    file_name="bestellungen.csv",
                    mime="text/csv"
                )
            
            with export_cols[1]:
                # Download as JSON
                st.write(create_download_link_json(
                    st.session_state.orders,
                    filename="bestellungen.json",
                    text="JSON herunterladen"
                ), unsafe_allow_html=True)
            
            with export_cols[2]:
                # Download as Text
                text_report = create_text_report(st.session_state.orders)
                st.write(create_download_link_text(
                    text_report,
                    filename="bestellungen.txt",
                    link_text="TXT herunterladen"
                ), unsafe_allow_html=True)
            
            with export_cols[3]:
                # Download as Image
                img = create_image_report(st.session_state.orders)
                st.write(create_download_link_image(
                    img,
                    filename="bestellungen.png",
                    link_text="PNG herunterladen"
                ), unsafe_allow_html=True)
        
        # Individual order actions
        with st.expander("Einzelne Bestellungen verwalten"):
            for i, order in enumerate(orders):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    order_type = order.get("type", "")
                    name = order.get("name", "")
                    
                    if order_type == "yamyam":
                        st.write(f"{name}: YamYam #{order.get('number')}")
                    
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
                        
                        st.write(f"{name}: {product}{box_type} ({shop})")
                    
                    elif order_type == "edeka":
                        product = order.get("product", "")
                        if product == "Salat":
                            st.write(f"{name}: {product} - {order.get('salatType', '')}")
                        elif product == "Bäcker":
                            st.write(f"{name}: {product} - {order.get('baeckerItem', '')}")
                        else:
                            st.write(f"{name}: {product}")
                    
                    else:
                        st.write(f"{name}: Unbekannte Bestellung")
                
                with col2:
                    if st.button("Löschen", key=f"delete_{i}"):
                        remove_order(i)
        
        # Action to clear all orders
        st.warning("⚠️ Achtung: Diese Aktion kann nicht rückgängig gemacht werden!")
        if st.button("Alle Bestellungen löschen", key="clear_all_orders"):
            confirmation = st.checkbox("Bestätigen: Alle Bestellungen unwiderruflich löschen?")
            if confirmation:
                clear_orders()
    
    if st.button("Zurück zur Restaurantauswahl", key="order_list_back"):
        change_view("main")
