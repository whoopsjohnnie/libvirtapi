
# 
# Copyright (c) 2022, John Grundback
# 

import simplejson as json
import yaml

from flask import request
from flask import Response
from flask_restful import Resource

# import libvirt

from libvirtapi.api.rest.resource.default import DefaultResource
from libvirtapi.dao.interface import InterfaceDao



# 
# InterfacesResource
# 
class InterfacesResource(DefaultResource):

    def dao(self, driver, hypervisor):
        return InterfaceDao(driver, hypervisor)

    def get(self, driver, hypervisor):

        try:

            if not driver:
                return self.render_not_exists(request)

            if not hypervisor:
                return self.render_not_exists(request)

            dao = self.dao(driver, hypervisor)
            names = dao.getEntityNames()

            items = []
            if names:
                for name in names:
                    items.append(
                        self.buildInterface(
                            dao.getEntity(name)
                        )
                    )

            return self.ok(
                items, 
                request
            )

        except Exception as e:
            print(e)
            return self.render_exception(e, request)

    # def post(self, driver, hypervisor):
    #     pass



# 
# InterfaceResource
# 
class InterfaceResource(DefaultResource):

    def dao(self, driver, hypervisor):
        return InterfaceDao(driver, hypervisor)

    def get(self, driver, hypervisor, name):

        try:

            if not driver:
                return self.render_not_exists(request)

            if not hypervisor:
                return self.render_not_exists(request)

            if not name:
                return self.render_not_exists(request)

            dao = self.dao(driver, hypervisor)
            ditem = dao.getEntity(name)
            if not ditem:
                return self.render_not_exists(request)

            item = self.buildInterface(
                ditem
            )

            return self.ok(
                item, 
                request
            )

        except Exception as e:
            print(e)
            return self.render_exception(e, request)

    # def put(self, driver, hypervisor, name):
    #     pass

    # def delete(self, driver, hypervisor, name):
    #     pass
