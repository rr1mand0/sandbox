require 'uri'
require 'net/https'
require "time"

action :manage do
  package_file = @new_resource.package_cache
  package_name = @new_resource.package_name
  if @new_resource.packages_url # retrieve package from packages server

    # Determine the full URL for the remote package
    package_filename = nil
    if @new_resource.package_version
      package_filename = "#{package_name}-#{@new_resource.package_version}.tbz"
    else
      package_filename = "#{package_name}.tbz"
    end
    full_package_url = "#{@new_resource.packages_url}/#{@new_resource.packages_category}/#{package_filename}"

    # We must store cached packages from different categories separately
    cache_dir = "#{::File.dirname(@new_resource.package_cache)}/#{@new_resource.packages_category}"
    Dir.mkdir(cache_dir) if !::File.exists?(cache_dir)
    package_file = "#{cache_dir}/#{package_filename}"

    Chef::Log.info("Going to reconcile #{package_file} with #{full_package_url}")

    # Prepare HTTPS session
    cookbook = run_context.cookbook_collection[@new_resource.cookbook_name]
    client_cert_path = cookbook.preferred_filename_on_disk_location(node, :files, @new_resource.client_cert)
    client_key_path = cookbook.preferred_filename_on_disk_location(node, :files, @new_resource.client_key)
    ca_cert_path = cookbook.preferred_filename_on_disk_location(node, :files, @new_resource.ca_cert)

    package_uri = URI.parse(full_package_url)
    client_cert_pem = ::File.read(client_cert_path)
    client_key_pem = ::File.read(client_key_path)
    http = Net::HTTP.new(package_uri.host, package_uri.port)
    http.use_ssl = true
    http.cert = OpenSSL::X509::Certificate.new(client_cert_pem)
    http.key = OpenSSL::PKey::RSA.new(client_key_pem)
    http.verify_mode = OpenSSL::SSL::VERIFY_PEER
    http.ca_file = ca_cert_path
    http.verify_depth = 1
    http.set_debug_output($stdout) if @new_resource.debug_https

    # Fetch the package
    request = Net::HTTP::Get.new(package_uri.request_uri)
    if ::File.exists?(package_file)
      request.add_field('If-Modified-Since', ::File.mtime(package_file).httpdate)
    end
    http.request(request) do |response|
      if response.is_a?(Net::HTTPNotModified)
        Chef::Log.info("Remote file is no newer than cached version, not downloading")
      else
        Chef::Log.info("Downloading package from #{full_package_url} => #{package_file}")
        begin
          response.value() # will raise exception if not 2xx
        rescue
          raise "#{full_package_url}: #{response.code} #{response.message}"
        end
        f = open(package_file, 'w')
        begin
          response.read_body do |segment|
            f.write(segment)
          end
        ensure
          f.close()
        end
      end
    end
  end

  aw_package_regex = "^#{package_name}-[0-9]+\.[0-9]+"
  installed_version = `pkg_info -E -X '#{aw_package_regex}'`
  if $? == 0 # Package is installed
    # Determine installed version
    match = installed_version.match("^#{package_name}-(.+)\s*")
    if match
      installed_version = match[1]
    else
      raise "Unable to parse version from: #{installed_version}"
    end
    Chef::Log.info("Version of currently installed package: #{installed_version}")

    # Determine candidate package version
    candidate_version = nil
    tar_out = `tar -O -xjf #{package_file} +CONTENTS`
    raise "Unable to extract candidate package's +CONTENTS file" if $? != 0
    tar_out.each do |line|
      groups = /^@name\s+#{package_name}-(.*)\s*$/.match(line)
        if groups && groups.length == 2
          candidate_version = groups[1]
          break
        end
    end
    raise 'Could not determine version of candidate package to install' if !candidate_version
    Chef::Log.info("Version of candidate package for install: #{candidate_version}")

    # Decide if we are going to upgrade
    if @new_resource.enable_upgrade &&
      (Gem::Version.new(candidate_version) > Gem::Version.new(installed_version) ||
       @new_resource.always_upgrade)
      # The commands to actually perform the upgrade (if necessary)
      Chef::Log.info("Going to upgrade #{package_name} package from #{installed_version} => #{candidate_version}")
      execute "pkg_delete -X '^aw-[0-9]+\.[0-9]+'"
      execute "pkg_add #{package_file}"
      @new_resource.updated_by_last_action(true) # indicate that we did something
    else
      Chef::Log.info("Not upgrading #{package_name} package")
    end
  else # Package is not installed
    Chef::Log.info("#{package_name} package not installed, will install")
    execute "pkg_add #{package_file}"
    @new_resource.updated_by_last_action(true) # indicate that we did something
  end
end
