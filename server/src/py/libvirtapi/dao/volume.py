
# 
# Copyright (c) 2022, John Grundback
# 

import libvirt

from libvirtapi.dao.dao import DaoError, Dao



# 
# Volume DAO class
# 
class VolumeDao(Dao):

    def __init__(self, pool, driver, hypervisor):
        super().__init__(driver, hypervisor)
        self.pool = pool

    # 
    # Volumes
    # 

    def getEntityNames(self):

        pool = self.pool
        if not pool:
            raise DaoError("No such pool")

        conn = self.conn()
        if not conn:
            # "Failed to open connection", 
            raise DaoError("Failed to open connection")

        names = None
        try:

            dpool = conn.storagePoolLookupByName(pool)
            if not dpool:
                raise DaoError("No such pool")

            names = dpool.listVolumes()

        except libvirt.libvirtError as e:
            conn.close()
            raise DaoError("Dao exception", e)

        conn.close()
        return names

    def getEntity(self, name):

        pool = self.pool
        if not pool:
            raise DaoError("No such pool")

        conn = self.conn()
        if not conn:
            # "Failed to open connection", 
            raise DaoError("Failed to open connection")

        entity = None
        try:

            dpool = conn.storagePoolLookupByName(pool)
            if not dpool:
                raise DaoError("No such pool")

            entity = dpool.storageVolLookupByName(name)

        except libvirt.libvirtError as e:
            conn.close()
            raise DaoError("Dao exception", e)

        conn.close()
        return entity

    def createEntity(self, data):

        pool = self.pool
        if not pool:
            raise DaoError("No such pool")

        body = data

        conn = self.conn()
        if not conn:
            # "Failed to open connection", 
            raise DaoError("Failed to open connection")

        entity = None
        try:

            dpool = conn.storagePoolLookupByName(pool)
            if not dpool:
                raise DaoError("No such pool")

            entity = dpool.createXML(body)

        except libvirt.libvirtError as e:
            conn.close()
            raise DaoError("Dao exception", e)

        conn.close()
        return entity

    def syncEntity(self, name, data):
        pass

    def deleteEntity(self, name):

        pool = self.pool
        if not pool:
            raise DaoError("No such pool")

        conn = self.conn()
        if not conn:
            # "Failed to open connection", 
            raise DaoError("Failed to open connection")

        try:

            dpool = conn.storagePoolLookupByName(pool)
            if not dpool:
                conn.close()
                raise DaoError("No such pool")

            entity = dpool.storageVolLookupByName(name)
            if not entity:
                conn.close()
                raise DaoError("No such volume")

            entity.wipe()
            entity.delete()

        except libvirt.libvirtError as e:
            conn.close()
            raise DaoError("Dao exception", e)

        conn.close()
