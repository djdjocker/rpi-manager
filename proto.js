'use strict';
var format = require('date-format');
var fs = require('fs');
const path = require('path');

global.Config = JSON.parse(fs.readFileSync(path.join(__dirname, "config.json")));

Date.prototype.format = function(f){
    return f ? format(f, this) : format(this);
}