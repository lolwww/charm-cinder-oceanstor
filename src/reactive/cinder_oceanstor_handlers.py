# Copyright 2019
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import charms_openstack.charm
import charms.reactive
from   charmhelpers.core.host import os

# This charm's library contains all of the handler code associated with
# this charm -- we will use the auto-discovery feature of charms.openstack
# to get the definitions for the charm.
import charms_openstack.bus
charms_openstack.bus.discover()

charms_openstack.charm.use_defaults(
    'charm.installed',
    'update-status',
    'upgrade-charm',
    'storage-backend.connected',
)

@charms.reactive.when('storage-backend.broken') 
@charms.reactive.when('driver_init_configured')
@charms.reactive.when_not('driver_file_removed')
def remove_driver_config():
    with charms_openstack.charm.provide_charm_instance() as charm:
        os.system("test -e %s && rm %s || :" % ( charm.driver_config_file_iscsi, charm.driver_config_file_iscsi ) )
        os.system("test -e %s && rm %s || :" % ( charm.driver_config_file_fc, charm.driver_config_file_fc ) )

    charms.reactive.set_flag('driver_file_removed')

@charms.reactive.when_not('driver_init_configured')
@charms.reactive.when('storage-backend.available')
def driver_config():
    charms.reactive.set_flag('config.changed')

@charms.reactive.when('config.changed')
@charms.reactive.when('storage-backend.available')
def render_config(*args):
    # Huawei cinder volume driver would modify driver_config_file (/etc/cinder/cinder_huawei_conf.xml) to hidden username and passwrod
    # so it requires owner by cinder:root
    with charms_openstack.charm.provide_charm_instance() as charm:
         charm.render_with_interfaces(args)

    os.system("chown cinder:root %s" % charm.driver_config_file_iscsi)
    os.system("chown cinder:root %s" % charm.driver_config_file_fc)
    charms.reactive.set_flag('driver_init_configured')
    charm.assess_status()
