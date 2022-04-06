from website import create_app
# import folium

app = create_app()

#this means only when we run the file not when we import , this line will be execute
#else if u import it will run the web server
if __name__ == '__main__':
    app.run(debug = False)

