action :create do
  puts "My name is #{new_resource.name}"
  Chef::Log.info("Creating #{@new_resource} at #{@new_resource.path}")
  template_variables = {}
  %w{name}.each do |a|
    template_variables[a.to_sym] = new_resource.send(a)
  end

  # refactor the root user
  execute "echo CREATE DATABASE IF NOT EXISTS #{node['mysql']['database']} |mysql -u root --password=#{node['mysql']['server_root_password']} "

  execute "cd /home/vagrant/src/www/crust && python manage.py syncdb --noinput"
  Chef::Log.info("Using variables #{template_variables} to configure #{@new_resource}")
end

