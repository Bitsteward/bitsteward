#!/usr/bin/python


from gi.repository import Gtk, Adw, GLib
import gi

from gi.repository import Pango
from dotenv import load_dotenv

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
load_dotenv()


class Id(Gtk.Widget):
    def init_ui(self, page):

        scrollView = Gtk.ScrolledWindow()
        scrollView.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC
        )
        scrollView.set_kinetic_scrolling(True)

        # content box
        content = Gtk.Box(
            spacing=10,
            margin_start=20,
            margin_end=20,
            margin_top=20,
            margin_bottom=20,
            orientation=Gtk.Orientation.VERTICAL
        )

        scrollView.set_child(content)

        # label
        vault_item_title = Gtk.Label(label=page["name"])
        vault_item_title.set_ellipsize(Pango.EllipsizeMode.END)
        vault_item_title.get_style_context().add_class('title-1')
        content.append(vault_item_title)


        ### ID listbox
        prefGroup_ID = Adw.PreferencesGroup (title = 'Personnal information')
        person = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        prefGroup_ID.add(person)
        person.get_style_context().add_class('boxed-list')
        content.append(prefGroup_ID)

        # First name
        row_fistName = Adw.EntryRow(title="First name")
        try:
            row_fistName.set_text(page["identity"]["firstName"])
        except:
            print(
                f"could not load firstName for id: {page['id']} ({page['name']})")
        person.append(row_fistName)

        # Middle name
        row_middleName = Adw.EntryRow(title="Middle name")
        try:
            row_middleName.set_text(page["identity"]["middleName"])
        except:
            print(
                f"could not load middleName for id: {page['id']} ({page['name']})")
        person.append(row_middleName)

        # Last name
        row_lastName = Adw.EntryRow(title="Last name")
        try:
            row_lastName.set_text(page["identity"]["lastName"])
        except:
            print(
                f"could not load lastName for id: {page['id']} ({page['name']})")
        person.append(row_lastName)

        # SSN
        row_ssn = Adw.PasswordEntryRow(title="Social security number")
        try:
            row_ssn.set_text(page["identity"]["ssn"])
        except:
            print(
                f"could not load SSN for id: {page['id']} ({page['name']})")
        person.append(row_ssn)

        # Passport number
        row_passportNbr = Adw.PasswordEntryRow(title="Passport number")
        try:
            row_passportNbr.set_text(page["identity"]["passportNumber"])
        except:
            print(
                f"could not load Passport number for id: {page['id']} ({page['name']})")
        person.append(row_passportNbr)


        ### Address listbox
        prefGroup_address = Adw.PreferencesGroup (title = 'Address')
        address = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        prefGroup_address.add(address)
        address.get_style_context().add_class('boxed-list')
        content.append(prefGroup_address)

        # Address1
        row_addr1 = Adw.EntryRow(title="Address 1")
        try:
            row_addr1.set_text(page["identity"]["address1"])
        except:
            print(
                f"could not load address1 for id: {page['id']} ({page['name']})")
        address.append(row_addr1)

        # Address2
        row_addr2 = Adw.EntryRow(title="Address 2")
        try:
            row_addr2.set_text(page["identity"]["address2"])
        except:
            print(
                f"could not load address2 for id: {page['id']} ({page['name']})")
        address.append(row_addr2)

        # Address3
        row_addr3 = Adw.EntryRow(title="Address 3")
        try:
            row_addr3.set_text(page["identity"]["address3"])
        except:
            print(
                f"could not load address3 for id: {page['id']} ({page['name']})")
        address.append(row_addr3)

        # Postal code
        row_postalCode = Adw.EntryRow(title="Postal code")
        try:
            row_postalCode.set_text(page["identity"]["postalCode"])
        except:
            print(
                f"could not load postalCode for id: {page['id']} ({page['name']})")
        address.append(row_postalCode)

        # Country
        row_country = Adw.EntryRow(title="Country")
        try:
            row_country.set_text(page["identity"]["country"])
        except:
            print(
                f"could not load country for id: {page['id']} ({page['name']})")
        address.append(row_country)

        # Province/state
        row_state = Adw.EntryRow(title="Provice/state")
        try:
            row_state.set_text(page["identity"]["state"])
        except:
            print(
                f"could not load state/province for id: {page['id']} ({page['name']})")
        address.append(row_state)

        # City
        row_city = Adw.EntryRow(title="City")
        try:
            row_city.set_text(page["identity"]["city"])
        except:
            print(
                f"could not load city for id: {page['id']} ({page['name']})")
        address.append(row_city)


        ### Contact info listbox
        prefGroup_contactInfo = Adw.PreferencesGroup (title = 'Contact information')
        contact_info = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        prefGroup_contactInfo.add(contact_info)
        contact_info.get_style_context().add_class('boxed-list')
        content.append(prefGroup_contactInfo)

        # Phone Number
        row_phoneNumber = Adw.EntryRow(title="Phone number")
        try:
            row_phoneNumber.set_text(page["identity"]["phone"])
        except:
            print(
                f"could not load phoneNumber for id: {page['id']} ({page['name']})")
        contact_info.append(row_phoneNumber)

        # Email
        row_email = Adw.EntryRow(title="Email")
        try:
            row_email.set_text(page["identity"]["email"])
        except:
            print(
                f"could not load email for id: {page['id']} ({page['name']})")
        contact_info.append(row_email)


        return scrollView
