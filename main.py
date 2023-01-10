import color_extractor
import uvicorn

def main():
    uvicorn.run(color_extractor.app, host='127.0.0.1', port=8005)

if __name__ == "__main__": main()