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
    $routeProvider.when('/accounts/login', {

        templateUrl: '/static/templates/authentication/login.html',
        controller: 'LoginController',
        controllerAs: 'vm'

      }).when('/accounts/users', {

        controller: 'ProjectController',
        controllerAs: 'pc',
        templateUrl: '/static/templates/authentication/user_all.html'

      }).otherwise({

        redirectTo: '/'
    });
    }
})();
