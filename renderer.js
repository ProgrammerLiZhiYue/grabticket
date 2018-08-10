// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
var http = require('http');
const format = require('date-fns/format');

function doNotify(evt) {
  http.get("http://free_bus_ticket.fyxmt.com/interface/ticketList?queryDate=" + format(new Date(), "YYYY-MM-DD"), res => {
    let r = '';
    res.on('data', chunk => {
      r += chunk;
    });
    res.on('end', () => {
      result = JSON.parse(r);
      if (result && result['success']) {
        let isNight = new Date().getHours() >= 19 || new Date().getHours() < 8;
        if (isNight) {
          id = result['obj']['busTrips'][0]['trips'][1]['id']
        }
        else {
          id = result['obj']['busTrips'][2]['trips'][0]['id']
        }
        sendData = { 'wechatNo': 'ofqo-uJLT6jux0jk8vm4vlPLIDCE', 'id': id }
      }
    })
  });












  sendData = getSendData("http://free_bus_ticket.fyxmt.com/interface/ticketList?queryDate=" + format(new Date(), "YYYY-MM-DD"), true);

  var options = {
    hostname: 'free_bus_ticket.fyxmt.com',
    path: '/interface/grabTicket',
    method: 'POST'
  };
  var req = http.request(options, res => {
    let r = '';
    let result;
    res.on('data', chunk => {
      r += chunk;
    });
    res.on('end', () => {
      result = JSON.parse(r);
    })
  });
  req.write(JSON.stringify(sendData));
  req.end();
}

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById("basic").addEventListener("click", doNotify1);
})