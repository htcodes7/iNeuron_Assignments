import pymongo


class MongoDBManagement:

    def __init__(self):
        self.url = "<give your mongoDB URL here>"

    def get_mongo_client(self):
        """
        This function creates the client object for connection purpose
        """
        try:
            mongo_client = pymongo.MongoClient(self.url)
            return mongo_client
        except Exception as e:

            raise Exception("(getMongoDBClientObject): Something went wrong on creation of client object\n" + str(e))

    def is_database_present(self, db_name):
        try:

            client = self.get_mongo_client()
            if db_name in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            raise Exception("(isDatabasePresent): Failed on checking if the database is present or not \n" + str(e))

    def is_collection_present(self, collection_name, db_name):

        try:
            database_status = self.is_database_present(db_name=db_name)
            if database_status:
                database = self.get_database(db_name=db_name)
                if collection_name in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                self.create_database(db_name=db_name)
                return False
        except Exception as e:
            raise Exception(f"(isCollectionPresent): Failed to check collection\n" + str(e))

    def create_database(self, db_name):
        try:
            database_check_status = self.is_database_present(db_name=db_name)
            if not database_check_status:
                client = self.get_mongo_client()
                print(client.list_database_names())
                database = client[db_name]
                initial_col = database['Initial']
                test_dict = {'initial': "this is initial document to create the database "}
                initial_col.insert_one(test_dict)
                print(client.list_database_names())
                client.close()
                return database
            else:
                client = self.get_mongo_client()
                database = client[db_name]
                client.close()
                return database
        except Exception as e:
            raise Exception(f"(createDatabase): Failed on creating database\n" + str(e))

    def create_collection(self, collection_name, db_name):
        try:
            collection_check_status = self.is_collection_present(collection_name=collection_name, db_name=db_name)
            if not collection_check_status:
                database = self.get_database(db_name=db_name)
                collection = database[collection_name]
                return collection
        except Exception as e:
            raise Exception(f"(createCollection): Failed to create collection {collection_name}\n" + str(e))

    def get_database(self, db_name):
        try:
            client = self.get_mongo_client()
            return client[db_name]
        except Exception as e:
            raise Exception(f"(getDatabase): Failed to get the database list")

    def create_document(self, db_name, collection_name, record):
        try:
            client = self.get_mongo_client()
            db_status = self.is_database_present(db_name=db_name)
            if db_status:

                collection_status = self.is_collection_present(collection_name=collection_name, db_name=db_name)
                if not collection_status:
                    database = client[db_name]
                    collection = database[collection_name]
                    collection.insert_one(record)
                    client.close()
        except Exception as e:
            raise Exception(f"(insertRecord): Something went wrong on inserting record\n" + str(e))

    def get_record_data(self, db_name, collection_name, query):
        client = self.get_mongo_client()
        database = client[db_name]
        collection = database[collection_name]
        records = collection.find_one(query)
        return records
