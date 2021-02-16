Huawie Oceanstor Storage Backend for Cinder
-------------------------------

Overview
========

This charm provides a Huawei oceanstor storage backend for use with the Cinder
charm.

To use:

    juju deploy cinder
    juju deploy cinder-oceanstor 
    juju add-relation cinder-oceanstor cinder

Configuration
=============
    The mimim configure with 

       juju config cinder-oceanstor --config config.yaml

    config.yaml example:
    cinder-oceanstor:
       username: admin  
       userpassword: admin 
       resturl: https://192.168.1.1:8088/deviceManager/rest/
       storagepool: StoragePool001 
       defaulttargetip: 192.168.1.2
      
    If it is not default storage, you can use it in OpenStack like below:
       openstack volume type create oceanstor --property volume_backend_name=oceanstor
       openstack volume create --size 1 --type oceanstor vol-iscsi-test
       
    charm cinder provide default-volume-type config to choose for multiple backends 

    to enable hypermetro
       juju config cinder-oceanstor hypermetro=true

See config.yaml for details of configuration options.

Limitations and to be enhanced 
=============
    - iSCSI and FC protocol support
    - multipath not tested yet
    - ALUA, FAILOVERMODE, PATHTYPE 
