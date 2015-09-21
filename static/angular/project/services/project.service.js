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
        project_all: project_all
    };

    return Project;

    function project_all() {
        return $http.post('/project/all',{

            /*if(Authentication.isAuthenticated()) {
                $location.url('/home');
            }*/
        });
    }

  }
})();