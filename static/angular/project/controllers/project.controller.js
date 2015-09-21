/**
* ProjectController
* @namespace djangoEMT.project.controllers
*/
(function () {
  'use strict';

  angular
    .module('djangoEMT.project.controllers')
    .controller('ProjectController', ProjectController);

  ProjectController.$inject = ['$location', '$scope', 'ProjectController'];

  /**
  * @namespace ProjectController
  */
  function ProjectController($location, $scope, ProjectController) {
    var pc = this;
    pc.project_all = project_all;

    /**
    * @name ProjectAll
    * @desc Show ProjectAll Page
    * @memberOf djangoEMT.project.controllers.ProjectController
    */
    function project_all() {
        Project.project_all();
    }
  }
})();