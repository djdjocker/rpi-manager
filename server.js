require('./proto');
require('./logger');

var http = require('http');
var path = require('path');
var server = require('express')();
var spawn = require('child_process').spawn;

Logger.level = (Config["general"] || {})["mode"] || 'info';
Logger.debug("Logger initialized");

server.get('/', function(req, res, next){
    res.send('Hello World!');
    next();
}).use(function (err, req, res, next) {
    Logger.error(err.stack || err);
    res.status(500).send('Something broke!');
}).use(function(req, res, next){
    Logger.info("Request", req.method, req.path, res.statusCode, res.statusMessage);
    res.end();
}).listen(8080, function(){
    Logger.info("Server start litening on port 8080");
    var gui = spawn("python",  [path.join(__dirname, 'gui.py')], {stdio: "inherit"});
    gui.on("close", function(){
        Logger.info("GUI closed, Closing process");
        process.exit();
    });
});