
# 
# Copyright (c) 2022, John Grundback
# 

import libvirt

from libvirtapi.dao.dao import DaoError, Dao



# 
# Interface DAO class
# 
class InterfaceDao(Dao):

    def __init__(self, driver, hypervisor):
        super().__init__(driver, hypervisor)

    # 
    # Interfaces
    # 

    def getEntityNames(self):

        conn = self.conn()
        if not conn:
            # "Failed to open connection", 
            raise DaoError("Failed to open connection")

        names = None
        try:

            print( conn.listAllInterfaces() )
            print( conn.listAllInterfaces() )

            # 
            # Does not include all active/inactive domains?
            # 
            # names = conn.()
            interfaces = conn.listAllInterfaces()
            names = []
            for interface in interfaces:
                names.append( interface.name() )

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

            entity = conn.interfaceLookupByName(name)

        except libvirt.libvirtError as e:
            conn.close()
            raise DaoError("Dao exception", e)

        conn.close()
        return entity

    def createEntity(self, data):
        pass

    def syncEntity(self, name, data):
        pass

    def deleteEntity(self, name):
        pass
