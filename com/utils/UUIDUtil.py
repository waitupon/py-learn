import uuid

class UUIDUtil (object):

    @staticmethod
    def getUUID():
        return str(uuid.uuid1()).replace("-","");