
# 
# Copyright (c) 2022, John Grundback
# 

import libvirt


# 
# DAO error class
# 
class DaoError(Exception):

    def __init__(self, error, exception = None):
        pass



# 
# DAO class
# 
class Dao():

    def __init__(self, driver, hypervisor):

        self.driver = driver
        self.hypervisor = hypervisor

    # def conn(self, driver, hypervisor):
    def conn(self):

        driver = self.driver
        hypervisor = self.hypervisor

        if not driver:
            raise DaoError("No driver defined")

        if not hypervisor:
            raise DaoError("No hypervisor defined")

        conn = libvirt.open( str(driver) + ":///" + str(hypervisor) )
        if not conn:
            # "Failed to open connection to " + str(driver) + ":///" + str(hypervisor), 
            raise DaoError(
                "Failed to open connection to " + str(driver) + ":///" + str(hypervisor)
            )

        return conn
