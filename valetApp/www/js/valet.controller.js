'use strict';

angular.module('valletApp').controller('ValetCtrl', ValetCtrl);
ValetCtrl.$inject = ['$scope'];

function ValetCtrl($scope) {
  var self = this;
  self.parkings = createParkings();
  self.status = 'Desconectado';

  var serverIp = '192.168.0.106';
  var wsuri = 'ws://' + serverIp + ':1017/ws';
  var connection = new autobahn.Connection({
    url: wsuri,
    realm: "realm1"
  });


  connection.onopen = function (session, details) {
    var t2 = 0;

    t2 = setInterval(function () {
      if (session.isOpen) {
        //if(settings.shutdown){
        session.call('com.mubo.serialvalue').then(
          function (res) {
            //console.log(res);
            WebSocketMessage(res);
            self.status = 'Conectado';
            //$cacheFactory('status').put(settings.shutdown, settings.shutdown);
          },
          function (err) {
            console.log("Erro para ler serial == ", err);
          }
        );
        //} else {
        //  clearInterval(t2);
        //  resetInfos();
        //}
      } else {
        console.log('Closed')
        //self.status = 'Desconectado';
        //reloadWatches();
      }
    }, 500);
  };

  connection.open();

  function createParkings() {
    var parking = [];
    for (var i = 0; i < 10; i++) {
      parking.push({ parkingNumber: i, active: 0 });
    }
    return parking;
  }

  function WebSocketMessage(message) {
    var content = [];
    if (typeof (message) === 'object') {
      console.log(message);
      content = message.message.split(',');
    } else {
      content = JSON.parse(message).message.split(',');
    }
    updateStatusPark(content);
    self.status = 'Conectado';
    reloadWatches();
  };

  function reloadWatches() {
    if (!$scope.$$phase) {
      $scope.$apply();
    }
  }

  function updateStatusPark(content) {
    content.forEach(function(parkStatus, index) {
      console.log(index);
      if(index === 0) {
        self.parkings[0].active = parseInt(parkStatus);
      } else if(index === 1) {
        self.parkings[4].active = parseInt(parkStatus);
      } else if(index === 2) {
        self.parkings[8].active = parseInt(parkStatus);
      }
    });
  }
}