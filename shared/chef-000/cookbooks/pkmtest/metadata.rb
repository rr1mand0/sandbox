maintainer        "Peter McAlpine"
maintainer_email  "peter.mcalpine@arcticwolf.com"
license           "All rights reserved"
description       "Does something which Peter is testing"
long_description  IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version           "0.0.1"
recipe            "pkmtest", "Includes the service recipe by default."
recipe            "pkmtest::alpha", "Configures the client.rb from a template."
recipe            "pkmtest::bravo", "Sets up a client daemon to run periodically"

%w{ freebsd }.each do |os|
  supports os
end
