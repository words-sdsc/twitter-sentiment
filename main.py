searchQuery = ""

# Get user search query
while(True):
    searchQuery = input("What search query would you like to track?\n")
    confirm = input("Is this query: \"%s\" correct? (y/n)")
    if confirm == "y" OR confirm == "Y":
        break

# Create the database inside of the twitter DB

