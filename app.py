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
from cloud_storage import CloudStorage

# Set page config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🍱",
    layout="wide"
)

# Initialize session state for navigation and UI state
if "current_view" not in st.session_state:
    st.session_state.current_view = "main"
if "selected_shop" not in st.session_state:
    st.session_state.selected_shop = None

# Initialize order manager if not already present
# This will automatically handle cloud persistence
if "order_manager" not in st.session_state:
    st.session_state.order_manager = OrderManager()

# Ensure orders are properly initialized in session state
# This maintains backward compatibility with existing code
if "orders" not in st.session_state:
    st.session_state.orders = st.session_state.order_manager.get_orders()
else:
    # Make sure order_manager has the latest orders if they were modified elsewhere
    if len(st.session_state.orders) != len(st.session_state.order_manager.orders):
        st.session_state.order_manager.orders = st.session_state.orders

def save_orders():
    """Save orders to persistent storage"""
    # Make sure OrderManager has the current list
    st.session_state.order_manager.orders = st.session_state.orders
    # Save orders
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
    # Save explicitly to ensure persistence
    st.session_state.order_manager.save_orders()
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

# Sidebar navigation
st.sidebar.title("LunchSquad 🍱")
st.sidebar.caption("Team Lunch Organizer")

# Navigation buttons
if st.sidebar.button("Hauptmenü", use_container_width=True):
    change_view("main")
    
if st.sidebar.button("Alle Bestellungen", use_container_width=True):
    change_view("order_list")

# Export/Import section in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Bestellungen verwalten")

if st.sidebar.button("Speichern", use_container_width=True):
    save_orders()

# Export options dropdown in sidebar
export_option = st.sidebar.selectbox(
    "Export Format",
    ["JSON", "CSV", "TXT", "Bild (PNG)"]
)

# Export button
if st.sidebar.button("Exportieren", use_container_width=True):
    if len(st.session_state.orders) == 0:
        st.sidebar.warning("Keine Bestellungen zum Exportieren vorhanden.")
    else:
        if export_option == "JSON":
            # Create download link for JSON
            json_href = create_download_link_json(st.session_state.orders)
            st.sidebar.markdown(f'<a href="{json_href}" download="lunch_orders.json">Download JSON</a>', unsafe_allow_html=True)
        
        elif export_option == "CSV":
            # Convert to dataframe and create CSV download link
            df = st.session_state.order_manager.get_orders_dataframe()
            csv_href = create_download_link(df)
            st.sidebar.markdown(f'<a href="{csv_href}" download="lunch_orders.csv">Download CSV</a>', unsafe_allow_html=True)
        
        elif export_option == "TXT":
            # Create text report and download link
            text_report = create_text_report(st.session_state.orders)
            txt_href = create_download_link_text(text_report)
            st.sidebar.markdown(f'<a href="{txt_href}" download="lunch_orders.txt">Download TXT</a>', unsafe_allow_html=True)
        
        elif export_option == "Bild (PNG)":
            # Create image report and download link
            img = create_image_report(st.session_state.orders)
            if img:
                img_href = create_download_link_image(img)
                st.sidebar.markdown(f'<a href="{img_href}" download="lunch_orders.png">Download PNG</a>', unsafe_allow_html=True)
            else:
                st.sidebar.error("Fehler beim Erstellen des Bildes.")

# Import orders from JSON
st.sidebar.markdown("---")
st.sidebar.subheader("Bestellungen importieren")
uploaded_file = st.sidebar.file_uploader("JSON Datei hochladen", type="json")
if uploaded_file is not None:
    try:
        imported_orders = json.load(uploaded_file)
        if isinstance(imported_orders, list):
            st.session_state.orders = imported_orders
            st.session_state.order_manager.orders = imported_orders
            st.session_state.order_manager.save_orders()
            st.sidebar.success(f"{len(imported_orders)} Bestellungen importiert.")
            st.rerun()
        else:
            st.sidebar.error("Ungültiges JSON-Format. Eine Liste von Bestellungen wird erwartet.")
    except Exception as e:
        st.sidebar.error(f"Fehler beim Import: {str(e)}")

# Reset orders button
if st.sidebar.button("Alle Bestellungen löschen", use_container_width=True):
    clear_confirm = st.sidebar.checkbox("Ich bin sicher, dass ich alle Bestellungen löschen möchte.")
    if clear_confirm:
        clear_orders()

# Main content based on current view
if st.session_state.current_view == "main":
    # Main selection view
    st.title("Restaurantauswahl")
    
    # Create a row of 3 columns for restaurant options
    col1, col2, col3 = st.columns(3)
    
    # YamYam option
    with col1:
        st.button(
            f"{YAMYAM_OPTIONS['icon']} {YAMYAM_OPTIONS['name']}",
            help=YAMYAM_OPTIONS['description'],
            on_click=change_view,
            args=["yamyam"],
            use_container_width=True
        )
        st.caption(YAMYAM_OPTIONS['description'])
    
    # Döner option
    with col2:
        st.button(
            f"{DONER_OPTIONS['icon']} {DONER_OPTIONS['name']}",
            help=DONER_OPTIONS['description'],
            on_click=change_view,
            args=["doner"],
            use_container_width=True
        )
        st.caption(DONER_OPTIONS['description'])
    
    # Edeka option
    with col3:
        st.button(
            f"{EDEKA_OPTIONS['icon']} {EDEKA_OPTIONS['name']}",
            help=EDEKA_OPTIONS['description'],
            on_click=change_view,
            args=["edeka"],
            use_container_width=True
        )
        st.caption(EDEKA_OPTIONS['description'])
    
    # Display current orders below
    st.markdown("---")
    st.subheader("Aktuelle Bestellungen")
    
    if len(st.session_state.orders) > 0:
        # Get formatted dataframe
        orders_df = st.session_state.order_manager.get_orders_dataframe()
        st.dataframe(orders_df, use_container_width=True)
    else:
        st.info("Noch keine Bestellungen vorhanden.")

elif st.session_state.current_view == "yamyam":
    # YamYam order form
    st.title(f"{YAMYAM_OPTIONS['icon']} {YAMYAM_OPTIONS['name']} Bestellung")
    
    # Add link to menu
    st.markdown("[Menükarte ansehen](https://asiayamyamimbiss.netlify.app/)")
    
    # Create form for order
    with st.form("yamyam_order_form"):
        name = st.text_input("Name:")
        number = st.text_input(f"Nummer (1-{YAMYAM_OPTIONS['max_number']}):")
        
        submitted = st.form_submit_button("Hinzufügen")
        if submitted:
            order = {
                "type": "yamyam",
                "name": name,
                "number": number
            }
            
            # Validate order
            valid, error_message = validate_yamyam_order(order)
            if valid:
                add_order(order)
            else:
                st.error(error_message)

elif st.session_state.current_view == "doner":
    # Döner order form
    st.title(f"{DONER_OPTIONS['icon']} {DONER_OPTIONS['name']} Bestellung")
    
    # Shop selection
    st.subheader("Wähle einen Laden:")
    
    # Shop selection buttons in a row
    shop_cols = st.columns(len(DONER_OPTIONS['shops']))
    for i, (col, shop_name, shop_value) in enumerate(zip(shop_cols, DONER_OPTIONS['shops'], DONER_OPTIONS['shop_values'])):
        with col:
            if st.button(shop_name, key=f"shop_{shop_value}", use_container_width=True):
                select_shop(shop_value)
    
    # If a shop is selected, show order form
    if st.session_state.selected_shop:
        # Show which shop is selected
        selected_shop_name = DONER_OPTIONS['shops'][DONER_OPTIONS['shop_values'].index(st.session_state.selected_shop)]
        st.success(f"Ausgewählter Laden: {selected_shop_name}")
        
        # Order form
        with st.form("doner_order_form"):
            name = st.text_input("Name:")
            
            # Product selection - angepasst an die Liste anstatt Dictionary
            product = st.selectbox("Produkt:", options=DONER_OPTIONS['products'])
            product_value = DONER_OPTIONS['product_values'][DONER_OPTIONS['products'].index(product)]
            
            # Box options (only shown if Dönerbox is selected)
            box_type = None
            if product == "Dönerbox":
                box_options = [f"{box_type}" for box_type in DONER_OPTIONS['box_types']]
                box_selection = st.radio("Box-Typ:", box_options)
                box_type = DONER_OPTIONS['box_values'][DONER_OPTIONS['box_types'].index(box_selection)]
            
            # Sauce selection (multiselect with max 2)
            st.write("Soßen (max. 2):")
            sauce_cols = st.columns(len(DONER_OPTIONS['sauces']))
            sauces = []
            for i, (col, sauce, sauce_value) in enumerate(zip(sauce_cols, DONER_OPTIONS['sauces'], DONER_OPTIONS['sauce_values'])):
                with col:
                    if st.checkbox(sauce, key=f"sauce_{sauce_value}"):
                        sauces.append(sauce_value)
            
            # Spice level
            spice_level = st.radio("Schärfegrad:", DONER_OPTIONS['spice_levels'])
            spice_value = DONER_OPTIONS['spice_values'][DONER_OPTIONS['spice_levels'].index(spice_level)]
            
            # Extras (multiselect with max 3)
            st.write("Extras (max. 3):")
            extras_cols = st.columns(3)  # Display in 3 columns for better layout
            extras = []
            for i, (extra, extra_value) in enumerate(zip(DONER_OPTIONS['extras'], DONER_OPTIONS['extra_values'])):
                with extras_cols[i % 3]:
                    if st.checkbox(extra, key=f"extra_{extra_value}"):
                        extras.append(extra_value)
            
            # Zusätzliches Freitext-Feld für individuelle Extras
            st.write("Oder eigene Extras eingeben:")
            custom_extra = st.text_input("Eigene Anmerkung:", key="custom_extra_input")
            
            submitted = st.form_submit_button("Hinzufügen")
            if submitted:
                # Bei leerem custom_extra nicht hinzufügen
                custom_extras = []
                if custom_extra.strip():
                    custom_extras = [f"custom:{custom_extra.strip()}"]
                
                # Create order object
                order = {
                    "type": "doner",
                    "shop": st.session_state.selected_shop,
                    "name": name,
                    "product": product_value,
                    "sauces": sauces,
                    "extras": extras + custom_extras,
                    "spiceLevel": spice_value
                }
                
                # Add box type if applicable
                if product_value == "box" and box_type:
                    order["boxType"] = box_type
                
                # Validate order
                valid, error_message = validate_doner_order(order)
                if valid:
                    add_order(order)
                else:
                    st.error(error_message)
    else:
        st.info("Bitte wähle zuerst einen Laden aus.")

elif st.session_state.current_view == "edeka":
    # Edeka order form
    st.title(f"{EDEKA_OPTIONS['icon']} {EDEKA_OPTIONS['name']} Bestellung")
    
    # Create form for order
    with st.form("edeka_order_form"):
        name = st.text_input("Name:")
        product = st.selectbox("Produkt:", EDEKA_OPTIONS['products'])
        
        # Conditional fields based on product selection
        salat_type = None
        sauce = None
        baecker_item = None
        custom_order = None
        
        if product == "Salat":
            salat_type = st.selectbox("Salat Auswahl:", EDEKA_OPTIONS['salads'])
            # Zusätzliches Freitext-Feld für Anmerkungen zum Salat
            custom_order = st.text_area("Zusätzliche Anmerkungen (optional):", 
                                         placeholder="z.B. Ohne Oliven, Extra Tomaten")
        elif product == "Bäcker":
            # Einfacher Ansatz mit Textfeld und Beschreibung
            st.markdown("### Bäcker Bestellung:")
            baecker_item = st.text_input("Freitext:", 
                                      value="", 
                                      placeholder="z.B. 2 Laugenbrötchen, 1 Nussschnecke")
        else:
            sauce = st.selectbox("Sauce:", EDEKA_OPTIONS['sauces'])
            # Zusätzliches Freitext-Feld für Sandwich und Wrap
            custom_order = st.text_area("Zusätzliche Anmerkungen (optional):", 
                                         placeholder="z.B. Ohne Gurken, Extra Käse")
        
        submitted = st.form_submit_button("Hinzufügen")
        if submitted:
            # Create order object
            order = {
                "type": "edeka",
                "name": name,
                "product": product
            }
            
            # Add salat type, sauce, baecker item, or custom order based on product
            if product == "Salat" and salat_type:
                order["salatType"] = salat_type
                # Füge Freitext hinzu, wenn vorhanden
                if custom_order and custom_order.strip():
                    order["customOrder"] = custom_order.strip()
            elif product == "Bäcker" and baecker_item:
                order["baeckerItem"] = baecker_item
            elif product != "Bäcker":  # Für Sandwich und Wrap (aber nicht für Bäcker)
                if sauce:
                    order["sauce"] = sauce
                # Füge Freitext hinzu, wenn vorhanden
                if custom_order and custom_order.strip():
                    order["customOrder"] = custom_order.strip()
            
            # Validate order
            valid, error_message = validate_edeka_order(order)
            if valid:
                add_order(order)
            else:
                st.error(error_message)

elif st.session_state.current_view == "order_list":
    # Order list view
    st.title("Bestellungen")
    
    if len(st.session_state.orders) > 0:
        # Get the formatted dataframe
        orders_df = st.session_state.order_manager.get_orders_dataframe()
        
        # Display dataframe with orders
        st.dataframe(orders_df, use_container_width=True)
        
        # Management options
        st.subheader("Bestellungen verwalten")
        
        # Allow removing specific orders
        with st.expander("Bestellung entfernen"):
            # Create a selectbox with order descriptions
            order_options = [f"{i+1}. {orders_df.iloc[i]['Name']} - {orders_df.iloc[i]['Restaurant']} - {orders_df.iloc[i]['Bestellung']}" 
                           for i in range(len(orders_df))]
            selected_order_idx = st.selectbox("Wähle eine Bestellung zum Entfernen:", 
                                           options=range(len(order_options)),
                                           format_func=lambda x: order_options[x])
            
            if st.button("Ausgewählte Bestellung entfernen"):
                remove_order(selected_order_idx)
        
        # Action to clear all orders
        st.warning("⚠️ Achtung: Diese Aktion kann nicht rückgängig gemacht werden!")
        
        # Initialisiere Checkbox-Status in session_state, falls nicht vorhanden
        if "confirm_clear_all" not in st.session_state:
            st.session_state.confirm_clear_all = False
            
        # Checkbox für Bestätigung (vor dem Button, damit sie nicht verschwindet)
        confirmation = st.checkbox(
            "Bestätigen: Alle Bestellungen unwiderruflich löschen?", 
            key="confirm_checkbox",
            value=st.session_state.confirm_clear_all
        )
        
        # Aktualisiere session_state basierend auf Checkbox
        st.session_state.confirm_clear_all = confirmation
        
        # Button zum Löschen
        if st.button("Alle Bestellungen löschen", key="clear_all_orders"):
            if st.session_state.confirm_clear_all:
                clear_orders()
            else:
                st.error("Bitte bestätige zuerst, dass du alle Bestellungen löschen möchtest.")
    else:
        st.info("Keine Bestellungen vorhanden.")
        
        # Add a button to go back to main view to add orders
        if st.button("Zurück zur Restaurantauswahl"):
            change_view("main")

# Footer with version info
st.markdown("---")
st.caption(f"LunchSquad v1.0.0 - Team Lunch Organizer")