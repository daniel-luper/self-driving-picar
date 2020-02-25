//declare required modules
var app = require('http').createServer(handler),
  io = require('socket.io').listen(app),
  static = require('node-static'),
  zerorpc = require('zerorpc');
app.listen(8080);

// Make a web server on port 8080
var file = new(static.Server)();
function handler(request, response)
{
  console.log('serving file',request.url)
  file.serve(request, response);
};

// Make a ZeroRPC client to connect to Python
var client = new zerorpc.Client({
  heartbeatInterval: null
});
client.connect("tcp://127.0.0.1:4242");

console.log('Pi Car server listening on port 8080 visit http://ipaddress:8080/socket.html');

// Fire up a web socket server, listen to cmds from the phone, and set pwm
io.sockets.on('connection', function (socket)
{
  // Pass on commands
  socket.on('fromclient', function (data)
  {
    // Activate auto-pilot for 'data.command' seconds
    if (!isNaN(data.command)) {
      client.invoke("auto", +data.command)
    // Exit
    } else if (data.command == "exit") {
      stop()
      process.exit()
    // Execute some other command
    } else {
      client.invoke(data.command)
    }
  });
});

// User hits ctrl+c
process.on('SIGINT', function()
{
  stop();
  console.log("\nGracefully shutting down from SIGINT (Ctrl-C)");

  return process.exit();
});

function stop()
{
  client.invoke('cleanup');
  console.log('### FULL STOP ###');
}
