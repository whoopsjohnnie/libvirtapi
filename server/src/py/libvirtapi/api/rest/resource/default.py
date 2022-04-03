
# 
# Copyright (c) 2022, John Grundback
# 

import logging
import traceback

import simplejson as json
import yaml

from flask import request
from flask import Response
from flask_restful import Resource

# import libvirt



class DefaultResource(Resource):

    # def conn(self, driver, hypervisor):
    # 
    #     if not driver:
    #         return self.render_not_exists(request)
    # 
    #     if not hypervisor:
    #         return self.render_not_exists(request)
    # 
    #     conn = libvirt.open( str(driver) + ":///" + str(hypervisor) )
    #     if not conn:
    #         return self.error(
    #             "Failed to open connection to " + str(driver) + ":///" + str(hypervisor), 
    #             request
    #         )
    # 
    #     return conn

    def getBody(self, request):
        if not request:
            return None
        # return request.json
        # return request.data
        if not request.data:
            return None
        return request.data.decode("utf-8")

    def getJSONBody(self, request):
        if not request:
            return None
        return request.json

    def buildDomain(self, domain):
        info = domain.info()
        return {
            "id": domain.ID(), 
            "name": domain.name(), 
            "uuid": domain.UUIDString(), 
            "autostart": domain.autostart(), 
            "active": domain.isActive(), 
            "persistent": domain.isPersistent(), 
            "state": info[0], 
            "memory": info[1], 
            "cpus": info[3], 
            "time": info[4], 
            "info": info
        }

    def buildPool(self, pool):

        volumes = 0
        if pool.isActive():
            volumes = pool.numOfVolumes()

        info = pool.info()
        return {
            # "id": pool.ID(), 
            "name": pool.name(), 
            "uuid": pool.UUIDString(), 
            "autostart": pool.autostart(), 
            "active": pool.isActive(), 
            "persistent": pool.isPersistent(), 
            # depends on pool.isActive()
            "volumes": volumes, 
            "state": info[0], 
            "capacity": info[1], 
            "allocation": info[2], 
            "available": info[3], 
            "info": info
        }

    def buildVolume(self, pool, volume):
        info = volume.info()
        return {
            # "id": volume.id, # volume.id(), 
            "name": volume.name(), 
            "info": info
        }

    def buildInterface(self, interface):
        # info = interface.info()
        return {
            # "id": interface.id, # interface.id(), 
            "name": interface.name(), 
            "active": interface.isActive(), 
            "mac": interface.MACString()
            # "info": info
        }

    def buildNetwork(self, network):
        # info = network.info()
        return {
            # "id": network.id, # network.id(), 
            "name": network.name(), 
            "uuid": network.UUIDString(), 
            "autostart": network.autostart(), 
            "active": network.isActive(), 
            "persistent": network.isPersistent(), 
            # "info": info
        }

    def ok(self, data, request):
        if request.headers and "Accept" in request.headers:
            if request.headers.get("Accept") == "application/yaml":
                return Response(yaml.dump(
                    data
                ), mimetype="application/yaml", status=200)
        return Response(json.dumps(
            data, 
            indent=4, 
            sort_keys=False
        ), mimetype="application/json", status=200)

    def bad(self, message, request):
        if request.headers and "Accept" in request.headers:
            if request.headers.get("Accept") == "application/yaml":
                return Response(yaml.dump({
                    "message": message
                }), mimetype="application/yaml", status=400)
        return Response(json.dumps({
                "message": message
            },
            indent=4, 
            sort_keys=False
        ), mimetype="application/json", status=400)

    def error(self, message, request):
        if request.headers and "Accept" in request.headers:
            if request.headers.get("Accept") == "application/yaml":
                return Response(yaml.dump({
                    "message": message
                }), mimetype="application/yaml", status=500)
        return Response(json.dumps({
                "message": message
            },
            indent=4, 
            sort_keys=False
        ), mimetype="application/json", status=500)

    def conflict(self, request):
        if request.headers and "Accept" in request.headers:
            if request.headers.get("Accept") == "application/yaml":
                return Response(yaml.dump({
                    "message": "conflict"
                }), mimetype="application/yaml", status=400)
        return Response(json.dumps({
                "message": "conflict"
            },
            indent=4, 
            sort_keys=False
        ), mimetype="application/json", status=400)

    def notfound(self, request):
        if request.headers and "Accept" in request.headers:
            if request.headers.get("Accept") == "application/yaml":
                return Response(yaml.dump({
                    "message": "notfound"
                }), mimetype="application/yaml", status=404)
        return Response(json.dumps({
                "message": "notfound"
            },
            indent=4, 
            sort_keys=False
        ), mimetype="application/json", status=404)

    def exception(self, exception, request):
        print(exception)
        traceback.print_exc()
        if request.headers and "Accept" in request.headers:
            if request.headers.get("Accept") == "application/yaml":
                return Response(yaml.dump({
                    "message": "exception",
                    "exception": str(exception)
                }), mimetype="application/yaml", status=500)
        return Response(json.dumps({
                "message": "exception",
                "exception": str(exception)
            },
            indent=4, 
            sort_keys=False
        ), mimetype="application/json", status=500)

    # deprecated
    def render_ok(self, data, request):
        return self.ok(data, request)

    # deprecated
    def render_error(self, message, request):
        return self.error(message, request)

    # deprecated
    def render_exists(self, request):
        return self.conflict(request)

    # deprecated
    def render_not_exists(self, request):
        return self.notfound(request)

    # deprecated
    def render_exception(self, exception, request):
        return self.exception(exception, request)
