(function () {
  'use strict';

  angular
    .module('djangoEMT.routes')
    .config(config);

  config.$inject = ['$routeProvider'];

  /**
  * @name config
  * @desc Define valid application routes
  */
    function config($routeProvider) {
    $routeProvider.when('/login', {
        controller: 'LoginController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/authentication/login.html'
      }).when('/home', {
        controller: 'HomeController',
        controllerAs: 'pc',
        templateUrl: '/static/templates/project/home.html'
      }).otherwise({
        redirectTo: '/login'
    });
    }
})();
