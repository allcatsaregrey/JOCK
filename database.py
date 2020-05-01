# Author: Matthew C. McFee
# Description: Database generation and relevant methods to store,
# manipulate, and reference auction IDs, and descriptions.

# TODO: Each key of the ID dictionary should contain a dictionary
# with keys such as start time, end time etc. so a full description
# of the auction is available. We also need to add functions to
# sort the auctions with in the database to certain specifications.


class jock_data_base():

    def __init__(self):

        self.db = {}

    def add_(self, id, desc):

        if id not in self.db:
            self.db[id] = desc

        else:
            print("Auction ID already present in database.")

    def del_(self, id):

        del self.dic[id]

    def search_id_(self, id):

        if id in self.db:
            print("ID exists in database.")

    def search_keywds_(self, keywds):

        id_matches = []

        for id, desc in self.db.items():
            for keywd in keywds:
                if keywd in desc.split():
                    id_matches.append(id)
        return id_matches

    def reinit_(self):

        self.db = {}


if __name__ == "__main__":
    print("Please run the main program file.")
