//declare required modules
var app = require('http').createServer(handler),
  io = require('socket.io').listen(app),
  static = require('node-static'),
  zerorpc = require('zerorpc');
app.listen(8080);

var speed = 0;
var left = 0;
var right = 0;
var leftSpeed;
var rightSpeed;
var minSpeed = 12;
var lastDirection = "";

var timer = "";

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
client.invoke('init');
client.invoke('forward');

console.log('Pi Car server listening on port 8080 visit http://ipaddress:8080/socket.html');

// Fire up a web socket server, listen to cmds from the phone, and set pwm
io.sockets.on('connection', function (socket)
{
  // Got phone msg
  socket.on('fromclient', function (data)
  {
    if (data.command == "update")
    {
      speed = data.speed;

      // Control the forward/backward direction
      if (speed >= 0 && lastDirection != "forward")
      {
        lastDirection = "forward";
        client.invoke('forward');
      } else if (speed < 0 && lastDirection != "backward"){
        lastDirection = "backward";
        client.invoke('reverse');
      }

      // Set pwm
      if (data.horizontal >= 0)
      {
        (data.horizontal < 0.1) ? right = 0 : right = data.horizontal
        left = 0;
      } else {
        (data.horizontal > -0.1) ? left = 0 : left = -data.horizontal
        right = 0;
      }
      rightSpeed = clip((1 - right) * speed);
      leftSpeed = clip((1 - left) * speed);

      console.log(rightSpeed);
      console.log(leftSpeed);
      client.invoke('move', leftSpeed, rightSpeed);

      // Exit if we haven't been connected for 2500 milliseconds
      clearInterval(timer);
      timer = setInterval(shutdown, 2500);
    } else if (data.command == "exit") {
      stop();
      process.exit();
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

// Return a pwm speed equal to 0 if less than 20
function clip(speed)
{
  speed = Math.abs(speed);
  if (speed < minSpeed){
    return 0;
  } else {
    return Math.min(speed, 100);
  }
}

// If we lose comms set the motors to neutral
function stop()
{
  client.invoke('stop')
  client.invoke('cleanup')
  console.log('### FULL STOP ###');
}

function shutdown()
{
  stop();
  client.invoke('shutdown');
  process.exit();
}
