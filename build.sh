export CHARM_DIR=~/charms
export CHARM_BUILD_DIR=$CHARM_DIR
export CHARM_LAYERS_DIR=$CHARM_DIR/layers
export CHARM_INTERFACES_DIR=$CHARM_DIR/interfaces
test -d $CHARM_DIR && rm -rf $CHARM_DIR
mkdir -p $CHARM_LAYERS_DIR $CHARM_INTERFACES_DIR 
charm build 
