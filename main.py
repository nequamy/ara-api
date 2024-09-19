from app import Api


def main():
    api = Api("192.168.2.1", 5760)
    
    api.update_loop()

if __name__ == "__main__":
    main()