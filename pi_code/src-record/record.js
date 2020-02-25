//declare required modules
var app = require('http').createServer(handler),
  io = require('socket.io').listen(app),
  static = require('node-static'),
  zerorpc = require('zerorpc');
app.listen(8080);

var speed = 0;
var leftSpeed = 0;
var rightSpeed = 0;
var reverse = false;
var lastDirection = "";
var MIN_SPEED = 5;
var MAX_SPEED = 23;

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
      if (speed >= 0) {
        reverse = false;
      } else {
        reverse = true;
      }

      // Establish how the car should interpret the steering
      if (data.horizontal > 0 && lastDirection != "right") {
        client.invoke('right');
        lastDirection = "right";
        leftSpeed = clip(speed);
        rightSpeed = MIN_SPEED;
      } else if (data.horizontal < 0 && lastDirection != "left") {
        client.invoke('left');
        lastDirection = "left";
        rightSpeed = clip(speed);
        leftSpeed = MIN_SPEED;
      } else if (data.horizontal == 0){
        if (reverse == false && lastDirection != "forward") {
          client.invoke('forward');
          lastDirection = "forward";
        } else if (reverse == true && lastDirection != "backward") {
          client.invoke('backward');
          lastDirection = "backward";
        }
        leftSpeed = clip(speed)
        rightSpeed = clip(speed)
      }

      // Set pwm
      client.invoke('move', leftSpeed, rightSpeed);

      // Shutdown if we haven't been connected for 3 seconds
      clearInterval(timer);
      timer = setInterval(shutdown, 3000);
    } else if (data.command == "shutdown") {
      shutdown();
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

// Return a pwm speed less than MAX_SPEED and equal to 0 if less than 20
function clip(speed)
{
  speed = Math.abs(speed);
  if (speed < MIN_SPEED) {
    return 0;
  } else {
    return MAX_SPEED;
  }
}

function stop()
{
  client.invoke('gpio_stop');
  client.invoke('cleanup');
  console.log('### FULL STOP ###');
}

function shutdown()
{
  stop();
  client.invoke('shutdown');
  process.exit();
}
