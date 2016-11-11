var path = require('path')
var childProcess = require('child_process')
var slimerjs = require('slimerjs')
var binPath = slimerjs.path
 
var childArgs = [
  path.join(__dirname, 'open_url.js'),
  'some'
]
var gobal = null;
 
childProcess.execFile(binPath, childArgs, function(err, stdout, stderr) {
    console.log("process close");
})

console.log('in main process');
