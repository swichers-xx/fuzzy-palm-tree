Remote Server Control and Monitoring
This project provides a set of RESTful API endpoints for controlling and monitoring remote Windows servers. It also includes a simple frontend service monitor built using React.  For ease of use, all servers and services are color coded red for down, or green for up.

Backend
The backend is written in Python using Flask, a popular lightweight web framework. It uses the flask_limiter and flask_basicauth modules for rate limiting and basic HTTP authentication, respectively.

Usage
The backend provides two main endpoints: /power and /service. Both are POST endpoints that accept JSON data in the request body. Here's what the request data should look like for each endpoint:

Power Control (/power)
json
{
"command": "Stop-Computer",
"server": "ServerName"
}

The command can be one of the following PowerShell commands: Stop-Computer, Restart-Computer, Suspend-Computer, Add-Computer, Rename-Computer, or Reset-ComputerMachinePassword.

Service Control (/service)
json
{
"command": "Get-Service",
"server": "ServerName",
"service_name": "ServiceName"
}

The command can be one of the following PowerShell commands: Get-Service, New-Service, Restart-Service, Resume-Service, Set-Service, Start-Service, Stop-Service, Suspend-Service, Enable-Service, or Disable-Service.

For both endpoints, the server name is a string representing the name of the target Windows server. The service name is a string representing the name of the target Windows service.

Both endpoints are rate-limited to 10 requests per minute and protected by HTTP Basic Authentication.

Running the Backend
To run the backend:

Install the dependencies with pip install flask flask_limiter flask_basicauth.
Run the script with python script.py.
Frontend
The frontend is a React component named ServiceMonitor. It uses Axios for HTTP requests and Material-UI for the table component.

Usage
The ServiceMonitor component fetches the status of any service with "Voxco" in the name on multiple servers, every time it is rendered. The servers it queries are defined in the servers array.

The servers() endpoint returns a list of servers and their current power status, color coded red for down, or green for up.

To run the frontend:

Install the dependencies with npm install react axios @material-ui/core.
Add the ServiceMonitor component to your React app and render it.
Note
Ensure that the servers you're trying to control or monitor are reachable from the machine running this code and that the appropriate permissions are set to allow the operations. Please replace the admin and adminpassword credentials with your own.

Remember to replace the hardcoded localhost URL in the axios request with your backend's URL when deploying this application in a production environment.

Please note that improper use of the /power and /service endpoints can lead to unexpected system states and should be used with caution.
