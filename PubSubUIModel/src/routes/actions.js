var express = require('express');
var router = express.Router();
var db = require('../database');

const ActionAdapter = require('../services/action.js');

router.put("/", function(req, res) {
  /*data = {
    deviceId: req.body.deviceId,
    action: req.body.action,
    status: "In progress",
    id: req.body.id,
  }
  console.log("data: ", data)
  db.Action.create(data)
  .then( action => {
    ActionAdapter.executePingAction(req.params.deviceId);
    res.status(200).send(JSON.stringify(action));
  })
  .catch( err => {
    res.status(500).send(JSON.stringify(err));
  });*/
  ActionAdapter.executePingAction(req.params.deviceId);
  res.status(200).send(JSON.stringify({
    "deviceId": req.body.deviceId,
    "action": req.body.action,
    "status": "In progress",
  }));
});

module.exports = router;