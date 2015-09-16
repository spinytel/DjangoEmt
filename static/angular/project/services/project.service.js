/**
* Project
* @namespace djangoEMT.project.services
*/
(function () {
  'use strict';

  angular
    .module('djangoEMT.project.services')
    .factory('Project', Project);

  Project.$inject = ['$http'];

  /**
  * @namespace Project
  * @returns {Factory}
  */
  function Project($http) {
    /**
    * @name Project
    * @desc The Factory to be returned
    */
    var Project = {
        home: home
    };

    return Project;

    function home() {
        return $http.post('/home/',{

            /*if(Authentication.isAuthenticated()) {
                $location.url('/home');
            }*/
        });
    }

  }
})();