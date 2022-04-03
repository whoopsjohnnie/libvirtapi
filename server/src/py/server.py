
# 
# Copyright (c) 2022, John Grundback
# 

from flask import Flask
from flask_restful import Resource, Api, reqparse

from libvirtapi.api.rest.resource.v10.domain import DomainsResource, DomainResource
from libvirtapi.api.rest.resource.v10.pool import PoolsResource, PoolResource
from libvirtapi.api.rest.resource.v10.volume import VolumesResource, VolumeResource
from libvirtapi.api.rest.resource.v10.interface import InterfacesResource, InterfaceResource
from libvirtapi.api.rest.resource.v10.network import NetworksResource, NetworkResource

app = Flask(__name__)
api = Api(app)

api.add_resource(DomainsResource, '/api/v1.0/<driver>/<hypervisor>/domain')
api.add_resource(DomainResource, '/api/v1.0/<driver>/<hypervisor>/domain/<name>')

api.add_resource(PoolsResource, '/api/v1.0/<driver>/<hypervisor>/pool')
api.add_resource(PoolResource, '/api/v1.0/<driver>/<hypervisor>/pool/<name>')

api.add_resource(VolumesResource, '/api/v1.0/<driver>/<hypervisor>/pool/<pool>/volume')
api.add_resource(VolumeResource, '/api/v1.0/<driver>/<hypervisor>/pool/<pool>/volume/<name>')

api.add_resource(NetworksResource, '/api/v1.0/<driver>/<hypervisor>/network')
api.add_resource(NetworkResource, '/api/v1.0/<driver>/<hypervisor>/network/<name>')

api.add_resource(InterfacesResource, '/api/v1.0/<driver>/<hypervisor>/interface')
api.add_resource(InterfaceResource, '/api/v1.0/<driver>/<hypervisor>/interface/<name>')

# if __name__ == "__main__":
app.run(
    host='0.0.0.0', port=8080
)
