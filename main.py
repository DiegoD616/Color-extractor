"""API - Main

This script allows the user to start a uvicorn server which runs the api's app

    * main - the main function of the script
"""
import api
import uvicorn

def main():
    uvicorn.run(api.app, host='127.0.0.1', port=8005)

if __name__ == "__main__": main()