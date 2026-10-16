from BACK.API.app import app

if __name__ == "__main__":
    
    app.run(
       
        host="127.0.0.1",
        port=2100,
        debug=False,
        use_reloader=False
    
    )
