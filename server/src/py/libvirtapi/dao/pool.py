
# 
# Copyright (c) 2022, John Grundback
# 

import libvirt

from libvirtapi.dao.dao import DaoError, Dao



# 
# Pool DAO class
# 
class PoolDao(Dao):

    def __init__(self, driver, hypervisor):
        super().__init__(driver, hypervisor)

    # 
    # Pools
    # 

    def getEntityNames(self):

        conn = self.conn()
        if not conn:
            # "Failed to open connection", 
            raise DaoError("Failed to open connection")

        names = None
        try:

            # 
            # Does not include all active/inactive pools?
            # 
            # names = conn.listDefinedStoragePools()
            pools = conn.listAllStoragePools()
            names = []
            for pool in pools:
                names.append( pool.name() )

        except libvirt.libvirtError as e:
            conn.close()
            raise DaoError("Dao exception", e)

        conn.close()
        return names

    def getEntity(self, name):

        conn = self.conn()
        if not conn:
            # "Failed to open connection", 
            raise DaoError("Failed to open connection")

        entity = None
        try:

            entity = conn.storagePoolLookupByName(name)

        except libvirt.libvirtError as e:
            conn.close()
            raise DaoError("Dao exception", e)

        conn.close()
        return entity

    def createEntity(self, data):

        body = data

        conn = self.conn()
        if not conn:
            # "Failed to open connection", 
            raise DaoError("Failed to open connection")

        entity = None
        try:

            # 
            # storagePoolCreateXML and storagePoolDefineXML have subtle differences
            # 
            # storagePoolCreateXML: 
            # storagePoolDefineXML: 
            # 
            # entity = conn.storagePoolCreateXML(body, 0)
            entity = conn.storagePoolDefineXML(body)

        except libvirt.libvirtError as e:
            conn.close()
            raise DaoError("Dao exception", e)

        conn.close()
        return entity

    def syncEntity(self, name, data):

        conn = self.conn()
        if not conn:
            # "Failed to open connection", 
            raise DaoError("Failed to open connection")

        entity = None
        try:

            entity = conn.storagePoolLookupByName(name)
            if entity:

                if "autostart" in data:
                    if data.get("autostart") == 0:
                        if( entity.autostart() ):
                            entity.setAutostart(0)
                    elif data.get("autostart") == 1:
                        if( not entity.autostart() ):
                            entity.setAutostart(1)
                    else:
                        raise DaoError("Invalid value for active, must be 0 or 1")

                if "active" in data:
                    if data.get("active") == 0:
                        if( entity.isActive() ):
                            entity.destroy()
                    elif data.get("active") == 1:
                        if( not entity.isActive() ):
                            entity.create()
                    else:
                        raise DaoError("Invalid value for active, must be 0 or 1")

            # fetch again
            entity = conn.storagePoolLookupByName(name)

        except libvirt.libvirtError as e:
            conn.close()
            raise DaoError("Dao exception", e)

        conn.close()
        return entity

    def deleteEntity(self, name):

        conn = self.conn()
        if not conn:
            # "Failed to open connection", 
            raise DaoError("Failed to open connection")

        try:

            ditem = conn.storagePoolLookupByName(name)
            if not ditem:
                conn.close()
                return None

            # 
            if ditem.isActive():
                ditem.shutdown()

            # 
            ditem.undefine()

        except libvirt.libvirtError as e:
            conn.close()
            raise DaoError("Dao exception", e)

        conn.close()
