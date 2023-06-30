import flask
from flask_limiter import Limiter
from flask_basicauth import BasicAuth
import json

app = flask.Flask(__name__)

# Create a rate limiter with a limit of 10 requests per minute
limiter = Limiter(app, key_prefix='remote_server_control', rate_limit=10)

# Create a basic HTTP authentication with username `admin` and password `adminpassword`
auth = BasicAuth(app)

@app.route('/power', methods=['POST'])
@limiter.limit('10/minute')
@auth.login_required
def power():
#  """
#  Controls the power state of a remote Windows server.
#
  Request body:
    {
      "command": "Stop-Computer",
      "server": "ServerName"
    }
  """

  request_data = request.get_json()
  command = request_data['command']
  server = request_data['server']

  # Execute the PowerShell command
  subprocess.run([
    'powershell',
    '-Command',
    command,
    '-ComputerName',
    server
  ])

  return 'Power state of server {} changed to {}'.format(server, command)

@app.route('/service', methods=['POST'])
@limiter.limit('10/minute')
@auth.login_required
def service():
  """
  Controls the status of a remote Windows service.

  Request body:
    {
      "command": "Get-Service",
      "server": "ServerName",
      "service_name": "ServiceName"
    }
  """

  request_data = request.get_json()
  command = request_data['command']
  server = request_data['server']
  service_name = request_data['service_name']

  # Execute the PowerShell command
  subprocess.run([
    'powershell',
    '-Command',
    command,
    '-ComputerName',
    server,
    '-ServiceName',
    service_name
  ])

  service_status = subprocess.check_output([
    'powershell',
    '-Command',
    'Get-Service -Name {} -ComputerName {} | Select-Object Status'.format(service_name, server)
  ]).decode('utf-8')
  service_status = json.loads(service_status)['Status']

  return 'Status of service {} on server {} is {}'.format(service_name, server, service_status)

def color_code_status(status):
  if status == 'Running':
    return 'green'
  elif status == 'Stopped':
    return 'red'
  else:
    return 'yellow'

@app.route('/servers')
@auth.login_required
def servers():
  """
  Returns a list of servers and their current power status, color coded red for down, or green for up.
  """

  servers = []
  for server in ['server1', 'server2', 'server3']:
    command = 'Get-Service -Name "W3SVC" -ComputerName {} | Select-Object Status'.format(server)
    service_status = subprocess.check_output([
      'powershell',
      '-Command',
      command
    ]).decode('utf-8')
    service_status = json.loads(service_status)['Status']
    servers.append({
      'server_name': server,
      'power_status': color_code_status(service_status)
    })

  return json.dumps(servers)

if __name__ == '__main__':
  app.run()
