import charms_openstack.charm
import charmhelpers.core.hookenv as ch_hookenv  # noqa

charms_openstack.charm.use_defaults('charm.default-select-release')


class CinderoceanstorCharm(
        charms_openstack.charm.CinderStoragePluginCharm):

    name = 'cinder_oceanstor'
    version_package = ''
    release = 'queens'
    packages = [version_package]
    release_pkg = ''
    stateless = True
    # Specify any config that the user *must* set.
    mandatory_config = ['username', 'userpassword', 'resturl', 'storagepool', 'defaulttargetip']
    driver_config_file_iscsi="/etc/cinder/cinder_huawei_conf.xml"
    driver_config_file_fc = "/etc/cinder/cinder_huawei_fc_conf.xml"

    restart_map = {driver_config_file_iscsi: ['cinder-volume'],
                   driver_config_file_fc: ['cinder-volume']}

    def cinder_configuration(self):
        drivers = {
            'iscsi': 'cinder.volume.drivers.huawei.huawei_driver.HuaweiISCSIDriver',
            'fc': 'cinder.volume.drivers.huawei.huawei_driver.HuaweiFCDriver',
        }

        volume_driver = drivers.get(self.config.get('protocol').lower())
        service = self.config.get('volume-backend-name')

        if self.config.get('protocol').lower() == "fc":
            driver_config_file = self.driver_config_file_fc
        elif self.config.get('protocol').lower() == "iscsi":
            driver_config_file = self.driver_config_file_iscsi
        else:
            print("Protocol unknown")

        driver_options = [
            ('volume_driver', volume_driver),
            ('cinder_huawei_conf_file', driver_config_file),
            ('volume_backend_name', service),
            # Add config options that needs setting on cinder.conf
        ]

        if self.config.get('hypermetro'):
            hypermetro_options = ('''storage_pool:{0},
            san_address:{1},
            san_user:{2},
            san_password:{3},
            vstore_name:{4},
            metro_domain:{5},
            metro_sync_completed:True, 
            fc_info: '{'HostName:xxx;ALUA:1;FAILOVERMODE:1;PATHTYPE:0'}'
            ''').format(self.config.get('storagepool'), self.config.get('resturl'),
                        self.config.get('username'), self.config.get('userpassword'),
                        self.config.get('vstorename'), self.config.get('metrodomain'))
            driver_options.append(('hypermetro_device', hypermetro_options))

        return driver_options


class CinderoceanstorCharmRocky(CinderoceanstorCharm):

    # Rocky needs py3 packages.
    release = 'rocky'
    version_package = ''
    packages = [version_package]
