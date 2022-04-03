
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
from libvirtapi.dao.volume import VolumeDao



# 
# VolumesResource
# 
class VolumesResource(DefaultResource):

    def dao(self, pool, driver, hypervisor):
        return VolumeDao(pool, driver, hypervisor)

    def get(self, driver, hypervisor, pool):

        try:

            if not driver:
                return self.render_not_exists(request)

            if not hypervisor:
                return self.render_not_exists(request)

            dao = self.dao(pool, driver, hypervisor)
            names = dao.getEntityNames()

            items = []
            if names:
                for name in names:
                    items.append(
                        self.buildVolume(
                            pool, 
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

    def post(self, driver, hypervisor, pool):

        try:

            if not driver:
                return self.render_not_exists(request)

            if not hypervisor:
                return self.render_not_exists(request)

            body = self.getBody(request)
            if not body:
                return self.bad("No pool XML definition found", request)

            dao = self.dao(pool, driver, hypervisor)
            nitem = dao.createEntity(body)
            if not nitem:
                return self.error("Unable to create pool", request)

            item = self.buildVolume(
                pool, 
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
# VolumeResource
# 
class VolumeResource(DefaultResource):

    def dao(self, driver, hypervisor, pool):
        return VolumeDao(driver, hypervisor, pool)

    def get(self, driver, hypervisor, pool, name):

        try:

            if not driver:
                return self.render_not_exists(request)

            if not hypervisor:
                return self.render_not_exists(request)

            if not name:
                return self.render_not_exists(request)

            dao = self.dao(pool, driver, hypervisor)
            ditem = dao.getEntity(name)
            if not ditem:
                return self.render_not_exists(request)

            item = self.buildVolume(
                pool, 
                ditem
            )

            return self.ok(
                item, 
                request
            )

        except Exception as e:
            print(e)
            return self.render_exception(e, request)

    def put(self, driver, hypervisor, pool, name):
        pass

    def delete(self, driver, hypervisor, pool, name):

        try:

            if not driver:
                return self.render_not_exists(request)

            if not hypervisor:
                return self.render_not_exists(request)

            if not name:
                return self.render_not_exists(request)

            dao = self.dao(pool, driver, hypervisor)
            dao.deleteEntity(name)

            return self.ok(
                {}, 
                request
            )

        except Exception as e:
            print(e)
            return self.render_exception(e, request)
