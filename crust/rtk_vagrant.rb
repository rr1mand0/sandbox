# rtk_vagrant.rb
# Shared utilities for Vagrant provisioning

require 'net/https'
require 'uri'
require 'base64'

class RTKVagrant

  INSTALL_CHEF_SH = File.expand_path(ENV['BUILDROOT']) + '/tools/install/install_chef.sh'
  TEMPLATE_ROOT_URL = 'https://packages01.cloud.arcticwolf.biz/templates/vagrant'
  CLIENT_CERT = ENV['BUILDROOT'] +
    '/chef/cookbooks/packages/files/default/etc/ssl/certs/packaging_client.cert.pem'
  CLIENT_KEY = ENV['BUILDROOT'] +
    '/chef/cookbooks/packages/files/default/etc/ssl/private/packaging_client.key.pem'
  CA_CERT = ENV['BUILDROOT'] +
    '/chef/cookbooks/awn/files/default/cloud.arcticwolf.biz-CA.cert.pem'

  ### Vagrant RsyncFile provisioner
  # Copy file(s) to the guest
  class RsyncFile < Vagrant::Provisioners::Base

    # Allow configuration of this provisioner
    class Config < Vagrant::Config::Base
      attr_accessor :delete
      attr_accessor :local_path
      attr_accessor :recursive
      attr_accessor :remote_path
      attr_accessor :verbose
    end

    def self.config_class
      Config
    end

    # SCP the file
    def provision!
      name = env[:vm].name
      config_temp = Tempfile.new('rsyncfile')
      config_temp.close
      system("vagrant ssh-config #{name} >#{config_temp.path}")
      system("cat #{config_temp.path}")
      recursive_opt = config.recursive ? '-r' : ''
      verbose_opt = (config.verbose || ENV['AWN_VERBOSE']) ? '-v' : '-q'
      delete_opt = config.delete ? '--delete' : ''
      quiet_opt = '' if config.verbose
      # Note '-L': transform symlink into referent file/dir
      cmd = "rsync -L #{verbose_opt} #{recursive_opt} #{delete_opt} " +
             "--rsh=\"ssh -F #{config_temp.path}\" " +
             "#{config.local_path} #{name}:#{config.remote_path}"
      env[:vm].ui.info "Going to execute:#{cmd}\n" if config.verbose
      system(cmd)
      config_temp.unlink
      if $? != 0 then raise "Unable to copy #{config.local_path} -> #{config.remote_path}" end
    end
  end

  ### Vagrant TemplateVersionCheck provisioner
  # Ensure the guest is using the most recent version of its template
  class TemplateVersionCheck < Vagrant::Provisioners::Base

    DEFAULT_SLEEP_SECONDS = 5

    # Allow configuration of this provisioner
    class Config < Vagrant::Config::Base
      attr_accessor :ca_cert
      attr_accessor :client_cert
      attr_accessor :client_key
      attr_accessor :sleep_seconds
      attr_accessor :template_root_url
      attr_accessor :template_name
      attr_accessor :verbose
    end

    def self.config_class
      Config
    end

    def prepare
      if config.ca_cert.nil?
        config.ca_cert = RTKVagrant::CA_CERT
      end
      if config.client_cert.nil?
        config.client_cert = RTKVagrant::CLIENT_CERT
      end
      if config.client_key.nil?
        config.client_key = RTKVagrant::CLIENT_KEY
      end
      if config.sleep_seconds.nil?
        config.sleep_seconds = DEFAULT_SLEEP_SECONDS
      end
      if config.template_name.nil?
        raise "Missing required 'template_name' attribute on template check provisioner"
      end
      if config.template_root_url.nil?
        config.template_root_url = RTKVagrant::TEMPLATE_ROOT_URL
      end
      if config.verbose.nil?
        config.verbose = false
      end
    end

    # Perform the template check
    def provision!
      latest_file_url = "#{config.template_root_url}/#{config.template_name}.latest"
      uri = URI.parse(latest_file_url)
      http = Net::HTTP.new(uri.host, uri.port)
      http.use_ssl = true
      http.verify_mode = OpenSSL::SSL::VERIFY_PEER
      http.cert = OpenSSL::X509::Certificate.new(::File.read(config.client_cert))
      http.key = OpenSSL::PKey::RSA.new(::File.read(config.client_key))
      http.ca_file = config.ca_cert
      http.verify_depth = 1
      env[:vm].ui.info "Going to fetch #{latest_file_url}..." if config.verbose
      response = http.get(latest_file_url)
      begin
        rc = response.value()
      rescue
        env[:vm].ui.info "Unable to perform template version check for template: #{config.template_name}"
        return
      end
      latest_version = response.body()
      env[:vm].ui.info "Latest version is #{latest_version}"
      begin
        env[:vm].channel.execute(<<eos
TEMPLATE_NAME=`cat /etc/awn_template_stamp | sed "s/=.*//"`
echo "Box template name is: $TEMPLATE_NAME" >&2
TEMPLATE_VERSION=`cat /etc/awn_template_stamp | sed "s/.*=//"`
echo "Box template version is: $TEMPLATE_VERSION" >&2
if [[ "$TEMPLATE_NAME" != "#{config.template_name}" || "$TEMPLATE_VERSION" != "#{latest_version}" ]]
then
  exit 1
fi
eos
)
        env[:vm].ui.info "Box template is up-to-date."
      rescue
        env[:vm].ui.warn "Box appears to be out of date. Please consider re-deploying your box as per these documents:"
        env[:vm].ui.warn "https://intranet.arcticwolf.com/pages/viewpage.action?pageId=4555034#HostLifecycleOpenstackVagrant-templatebuilder"
        env[:vm].ui.warn "https://intranet.arcticwolf.com/display/AWD/Test+Environment+Creation"
        env[:vm].ui.warn "Sleeping for #{config.sleep_seconds} seconds..."
        sleep(config.sleep_seconds)
      end
   end
  end

  ### Basebox utilities
  def self.get_base_box_url(box)
    path = File.expand_path(box, "#{ENV['HOME']}/.vagrant.d/aw-boxen")
    return path if File.exists?(path)

    # no local copy, use the URL
    return "#{TEMPLATE_ROOT_URL}/#{box}"
  end

  ### Provisioning utilities
  # Ubuntu's stock /root/.profile blindly calls 'mesg n' which causes 'stdin: not a tty' to
  # be outputted whenever we run vagarnt shell provisioners. This fixes that.
  # Note: This provisioner outputs the error it's trying to prevent (the first time it's run).
  def self.fix_root_profile(cfg)
    cfg.vm.provision :shell, :inline => "sed -i 's/^mesg n$/if [ `tty -s` ]; then mesg n; fi/' /root/.profile"
  end

  ### Install chef & disable chef-client daemon
  def self.install_chef(cfg)
    cfg.vm.provision RsyncFile do |provisioner|
      provisioner.local_path = INSTALL_CHEF_SH
      provisioner.remote_path = '/home/vagrant/install_chef.sh'
    end
    cfg.vm.provision :shell, :inline => "/home/vagrant/install_chef.sh"
  end

  def self.hostname2ip(hostname)
    result = {}
    Socket.getaddrinfo(hostname, 'http').map{|a| result.update a[0] => a[3]}
    return result['AF_INET']
  end
end

#
# Vagrant monkey patches
#   Vagrant doesn't support HTTPS server cert validation yet. These monkey
#   patches add this.
#   @mitchellh (Vagrant dev) promises version 1.2 will support server cert
#   validation as part of the Vagrant::Dwnloaders::HTTP class.
#

# Monkey patch 1.0.6
module Vagrant
  module Action
    module Box
      class Download
        def initialize(app, env)
          @app = app
          @env = env
          @env["download.classes"] ||= []
          @env["download.classes"] += [Downloaders::AWNHTTPS]
          @downloader = nil
        end
      end
    end
  end
end

# Monkey patch 1.1.0
class Vagrant::Action::Builtin::BoxAdd
  def download_klass(url)
    return Vagrant::Downloaders::AWNHTTPS
  end
end

# The HTTPS downloader which performs server cert validation
# This is based on 1.0.6's Vagrant::Downloaders::HTTP class
module Vagrant
  module Downloaders
    # Downloads a file from an HTTP URL to a temporary file. This
    # downloader reports its progress to stdout while downloading.
    class AWNHTTPS < Base
      def self.match?(uri)
        extracted = URI.extract(uri).first
        extracted && extracted.include?(uri)
      end

      def download!(source_url, destination_file)

        # Prepare HTTPS session
        uri = URI.parse(source_url)
        http = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl = true
        http.verify_mode = OpenSSL::SSL::VERIFY_PEER
        http.cert = OpenSSL::X509::Certificate.new(::File.read(RTKVagrant::CLIENT_CERT))
        http.key = OpenSSL::PKey::RSA.new(::File.read(RTKVagrant::CLIENT_KEY))
        http.ca_file = RTKVagrant::CA_CERT
        http.verify_depth = 1

        http.start do |h|
          h.request_get(uri.request_uri) do |response|
            if response.is_a?(Net::HTTPRedirection)
              download!(response["Location"], destination_file)
              return
            elsif !response.is_a?(Net::HTTPOK)
              raise Errors::DownloaderHTTPStatusError, :status => response.code
            end

            total = response.content_length
            progress = 0
            segment_count = 0

            response.read_body do |segment|
              # Report the progress out
              progress += segment.length
              segment_count += 1

              # Progress reporting is limited to every 25 segments just so
              # we're not constantly updating
              if segment_count % 25 == 0
                @ui.clear_line
                @ui.report_progress(progress, total)
                segment_count = 0
              end

              # Store the segment
              destination_file.write(segment)
            end

            # Clear the line one last time so that the progress meter disappears
            @ui.clear_line
          end
        end
      rescue SocketError
        raise Errors::DownloaderHTTPSocketError
      end
    end
  end
end
