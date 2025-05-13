import sys

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print("On branch main\nnothing to commit, working tree clean")
    else:
        print("Unknown command:", sys.argv[1:] if len(sys.argv) > 1 else "")

if __name__ == "__main__":
    main()
