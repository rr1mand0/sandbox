import os
env = Environment(ENV = os.environ)

def pytest_builder(source, target, env, for_signature):
  return env.Command(target[0], [ source ],
      [ 'python %s' % (source[0]), 'touch %s' % target[0] ])


pytest_spec_builder = Builder(
  generator = pytest_builder,
  prefix = '.',
  suffix = '.py.passed',
  src_suffix = '.py')
env.Append(BUILDERS = {'PyTestBuilder':  pytest_spec_builder})

pytest_file_list = []
for f in Glob('python/*/*_test.py'):
  test_target = env.PyTestBuilder(f)
  pytest_file_list.append(test_target)

env.Alias('pytest', pytest_file_list)
Default(pytest_file_list)

# vim: ft=python
