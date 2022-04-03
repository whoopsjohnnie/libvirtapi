
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
from libvirtapi.dao.network import NetworkDao



# 
# NetworksResource
# 
class NetworksResource(DefaultResource):

    def dao(self, driver, hypervisor):
        return NetworkDao(driver, hypervisor)

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
                        self.buildNetwork(
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

    def post(self, driver, hypervisor):

        try:

            if not driver:
                return self.render_not_exists(request)

            if not hypervisor:
                return self.render_not_exists(request)

            body = self.getBody(request)
            if not body:
                return self.bad("No network XML definition found", request)

            dao = self.dao(driver, hypervisor)
            nitem = dao.createEntity(body)
            if not nitem:
                return self.error("Unable to create network", request)

            item = self.buildNetwork(
                nitem
            )

            return self.ok(
                item, 
                request
            )

        except Exception as e:
            print(e)
            return self.render_exception(e, request)



# 
# NetworkResource
# 
class NetworkResource(DefaultResource):

    def dao(self, driver, hypervisor):
        return NetworkDao(driver, hypervisor)

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

            item = self.buildNetwork(
                ditem
            )

            return self.ok(
                item, 
                request
            )

        except Exception as e:
            print(e)
            return self.render_exception(e, request)

    def put(self, driver, hypervisor, name):

        try:

            if not driver:
                return self.render_not_exists(request)

            if not hypervisor:
                return self.render_not_exists(request)

            if not name:
                return self.render_not_exists(request)

            body = self.getJSONBody(request)
            if not body:
                return self.bad("No network JSON definition found", request)

            dao = self.dao(driver, hypervisor)
            ditem = dao.syncEntity(name, body)
            if not ditem:
                return self.render_not_exists(request)

            item = self.buildNetwork(
                ditem
            )

            return self.ok(
                item, 
                request
            )

        except Exception as e:
            print(e)
            return self.render_exception(e, request)

    def delete(self, driver, hypervisor, name):

        try:

            if not driver:
                return self.render_not_exists(request)

            if not hypervisor:
                return self.render_not_exists(request)

            if not name:
                return self.render_not_exists(request)

            dao = self.dao(driver, hypervisor)
            dao.deleteEntity(name)

            return self.ok(
                {}, 
                request
            )

        except Exception as e:
            print(e)
            return self.render_exception(e, request)
