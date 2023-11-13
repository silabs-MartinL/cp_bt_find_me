# Application imports
from App import App

# Create app
app = App(True)
# Main loop
loop = True
while loop:
    # Call app main function
    loop = app.main()