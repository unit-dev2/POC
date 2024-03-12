var express = require('express');
var router = express.Router();
var db = require('../database');

router.get("/all", function(req, res) {
    db.Device.findAll()
        .then( devices => {
            res.status(200).send(JSON.stringify(devices));
        })
        .catch( err => {
            res.status(500).send(JSON.stringify(err));
        });
});

router.get("/:id", function(req, res) {
    db.Device.findByPk(req.params.id)
        .then( device => {
            res.status(200).send(JSON.stringify(device));
        })
        .catch( err => {
            res.status(500).send(JSON.stringify(err));
        });
});

router.put("/", function(req, res) {
    db.Device.create({
        name: req.body.name,
        gcloudId: req.body.gcloudId,
        id: req.body.id
        })
        .then( device => {
            res.status(200).send(JSON.stringify(device));
        })
        .catch( err => {
            res.status(500).send(JSON.stringify(err));
        });
});

router.delete("/:id", function(req, res) {
    db.Device.destroy({
        where: {
            id: req.params.id
        }
        })
        .then( () => {
            res.status(200).send();
        })
        .catch( err => {
            res.status(500).send(JSON.stringify(err));
        });
});

module.exports = router;