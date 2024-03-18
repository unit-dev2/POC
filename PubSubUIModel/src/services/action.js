// const exec = require('child_process').exec;
const { spawn } = require('node:child_process');
const cliProgress = require('cli-progress');

const opt = {
  format: "Action: 'Ping' | progress: [{bar}] {percentage}% | Time left: {eta}s | {value}/{total}"
}

const classicProgressBar = new cliProgress.SingleBar(opt, cliProgress.Presets.shades_classic);

class ActionAdapter {

  static executePingAction() {
    let isStarted = false    
    const ping = spawn('ping', ['-w', '20', "localhost"]);

    ping.stdout.on('data', (data) => {
      if (!isStarted) {
        classicProgressBar.start(20, 0);
        isStarted = true
      } else {
        classicProgressBar.increment();
      }
    });
    
    ping.on('close', (code) => {      
    });
    
    ping.on('exit', (code) => {
      classicProgressBar.stop();
    }); 
  }
}

module.exports = ActionAdapter;