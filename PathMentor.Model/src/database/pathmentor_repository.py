class PathMentorRepository:
    def __init__(self, configuration, secrets, database_factory):
        self.configuration = configuration
        self.secrets = secrets
        self.database_factory = database_factory
        self.client = database_factory.get_client(self.secrets['SRV_URI'])
        self.database = self.client[self.configuration['database']]
        self.ensure_collections()

    def ensure_collections(self):
        required_collections = [self.configuration['train_collection'], self.configuration['test_collection']]
        existing_collections = self.database.list_collection_names()
        for collection in required_collections:
            if collection not in existing_collections:
                self.database.create_collection(collection)

    def store_records(self, collection, records):
        writer = self.database_factory.create_writer(self.secrets['SRV_URI'], self.configuration['database'], collection)
        for record in records:
            writer.write(record)

    def clear_collection(self, collection):
        self.database[collection].delete_many({})

    def drop_collection(self, collection):
        self.database.drop_collection(collection)
