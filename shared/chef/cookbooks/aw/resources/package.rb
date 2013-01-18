actions :manage
default_action :manage

# name of package
attribute :package_name, :kind_of => String, :name_attribute => true

# version of package, ignored if packages_url is set.
#   If false will retrieve the most recent version from the the packages server
attribute :package_version # false will auto-select the most recent version

# location on the local filesystem to store downloaded packages
attribute :package_cache, :kind_of => String, :required => true

# url for the packages server. If false will only examine the file at packages_cache
attribute :packages_url # false will just use the file in package_cache

# package category to download from the packages server. Ignored if packages_url is false
attribute :packages_category, :kind_of => String, :default => 'dev'

# SSL key/certs for communicating with packages_url
attribute :client_key, :kind_of => String, :required => true
attribute :client_cert, :kind_of => String, :required => true
attribute :ca_cert, :kind_of => String, :required => true

# Installs will always happen if package is not installed, if true upgrades are also enabled
attribute :enable_upgrade, :default => true

# Always upgrade even if the same or older version is installed, enable_upgrade must be true
attribute :always_upgrade, :default => false

# Output the HTTPS session for troubleshooting purposes
attribute :debug_https, :default => false
