from rest_api import app, menu_items

menu_items.append(
    {
        "name": "Settings",
        "tooltip": "Settings are here",
        "icon": "bx-grid-alt"
})
menu_items.append(
    {
        "name": "Settings 2",
        "tooltip": "Settings are here",
        "icon": "bx-grid-alt"
})
if __name__ =="__main__":
    app.run()
