/**
* HomeController
* @namespace djangoEMT.project.controllers
*/
(function () {
  'use strict';

  angular
    .module('djangoEMT.project.controllers')
    .controller('HomeController', HomeController);

  HomeController.$inject = ['$location', '$scope', 'HomeController'];

  /**
  * @namespace HomeController
  */
  function HomeController($location, $scope, HomeController) {
    var pc = this;
    pc.home = home;

    /**
    * @name Home
    * @desc Show Home Page
    * @memberOf djangoEMT.project.controllers.HomeController
    */
    function home() {
        Project.home();
    }
  }
})();