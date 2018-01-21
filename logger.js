'use strict';

const fs = require('fs');
const path = require('path');
const winston = require('winston');

const filename = path.join(__dirname, 'log', 'server.log');

function timestamp(){
    var now = new Date();
    return now.format('yyyy-MM-dd hh:mm:ss,SSS');
}

function formatter(options){
    var level = "[" + options.level.toUpperCase() +"]";
    level += " ".repeat(10 - level.length);
    
    var output = (options.colorize ? winston.config.colorize("silly", "[SRV] ") : "[SRV] ")
               + (options.colorize ? winston.config.colorize(options.level, level) : level) + " "
               + timestamp() + ': '
               + options.message;

    var meta = options.meta;
    
    if (meta !== null && meta !== undefined) {
        if (meta && meta instanceof Error && meta.stack) {
            meta = meta.stack;
        }

        if (typeof meta !== 'object') {
            output += ' ' + meta;
        }
        else if (Object.keys(meta).length > 0) {
            if (typeof options.prettyPrint === 'function') {
                output += ' ' + options.prettyPrint(meta);
            } else if (options.prettyPrint) {
                output += ' ' + '\n' + util.inspect(meta, false, options.depth || null, options.colorize);
            } else if (
                 options.humanReadableUnhandledException
              && Object.keys(meta).length >= 5
              && meta.hasOwnProperty('date')
              && meta.hasOwnProperty('process')
              && meta.hasOwnProperty('os')
              && meta.hasOwnProperty('trace')
              && meta.hasOwnProperty('stack')) {

                //
                // If meta carries unhandled exception data serialize the stack nicely
                //
                var stack = meta.stack;
                delete meta.stack;
                delete meta.trace;
                output += ' ' + exports.serialize(meta);

                if (stack) {
                  output += '\n' + stack.join('\n');
                }
            } else {
                output += ' ' + exports.serialize(meta);
            }
        }
    }

    return output;
}

const logger = new winston.Logger({
  transports: [
    new winston.transports.Console({
        colorize: true,
        timestamp: timestamp,
        formatter: formatter,
    }),
    new winston.transports.File({
        filename: filename, 
        json: false,
        timestamp: timestamp,
        formatter: formatter,
    })
  ]
});

global.Logger = logger