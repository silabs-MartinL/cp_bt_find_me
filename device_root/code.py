# Application imports
from App import App

# Create app
app = App(True)
# Main loop
while app.on:
    # Call app main function
    app.main()