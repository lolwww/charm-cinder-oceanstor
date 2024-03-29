import charms_openstack.charm
import charmhelpers.core.hookenv as ch_hookenv  # noqa

charms_openstack.charm.use_defaults('charm.default-select-release')

MULTIPATH_PACKAGES = [
    'multipath-tools',
    'sysfsutils',
]


class ProtocolNotImplemented(Exception):
    """Unsupported protocol error."""


class CinderoceanstorCharm(charms_openstack.charm.CinderStoragePluginCharm):

    name = 'cinder_oceanstor'
    # Package to determine application version
    version_package = 'cinder-common'
    release = 'queens'
    packages = MULTIPATH_PACKAGES
    release_pkg = version_package
    stateless = True

    # Specify any config that the user *must* set.
    mandatory_config = [
        'username', 'userpassword', 'resturl', 'storagepool', 'protocol'
    ]
    driver_config_file = "/etc/cinder/cinder_huawei_conf.xml"
    restart_map = {
        driver_config_file: ['cinder-volume']
    }

    def cinder_configuration(self):
        self.config['username'] = self.config.get('username').strip()
        self.config['userpassword'] = self.config.get('userpassword').strip()

        base_driver = 'cinder.volume.drivers.huawei.huawei_driver.{0}'
        drivers = {
            'iscsi': base_driver.format('HuaweiISCSIDriver'),
            'fc': base_driver.format('HuaweiFCDriver'),
        }

        protocol = self.config.get('protocol').lower()
        if protocol not in ['fc', 'iscsi']:
            raise ProtocolNotImplemented(
                "{0} is not an implemented protocol. Please, choose between "
                "`iscsi` and `fc`.".format(protocol)
            )

        use_mpath_img_xfer = self.config.get('use-multipath-for-image-xfer')
        enforce_multipath = self.config.get('enforce-multipath-image-xfer')

        driver_options = [
            (
                'volume_driver',
                drivers.get(self.config.get('protocol').lower())
            ),
            ('cinder_huawei_conf_file', self.driver_config_file),
            ('volume_backend_name', self.config.get('volume-backend-name')),
            ('use_multipath_for_image_xfer', use_mpath_img_xfer),
            ('enforce_multipath_for_image_xfer', enforce_multipath)
        ]

        if self.config.get('hypermetro'):
            config_keys = [
                'storagepool', 'resturl', 'username', 'userpassword',
                'vstorename', 'metrodomain'
            ]

            for k in config_keys:
                if not self.config.get(k):
                    raise ProtocolNotImplemented(
                        "HyperMetro init error: {0} option is required".format(
                            k
                        )
                    )
            hypermetro_options = ('''storage_pool:{0},
            san_address:{1},
            san_user:{2},
            san_password:{3},
            vstore_name:{4},
            metro_domain:{5},
            metro_sync_completed:True,
            fc_info: '{'HostName:xxx;ALUA:1;FAILOVERMODE:1;PATHTYPE:0'}'
            ''').format(
                self.config.get('storagepool'),
                self.config.get('resturl'),
                self.config.get('username'),
                self.config.get('userpassword'),
                self.config.get('vstorename'),
                self.config.get('metrodomain')
            )
            driver_options.append(('hypermetro_device', hypermetro_options))

        return driver_options
