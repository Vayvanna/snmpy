#this is the file that'll be the entry point to the app, 
# it'll start the web server using Flask
# and start the background tasks (ping & snmp polls)
from app import create_app  ##importing the function that creates the app.

app=create_app()
## call and save in app

# start the server in debug mode
if __name__== '__main__':
    app.run(debug=True)