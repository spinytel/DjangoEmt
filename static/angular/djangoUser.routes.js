(function () {
  'use strict';

  angular
    .module('djangoUser.routes')
    .config(config);

  config.$inject = ['$routeProvider'];

  /**
  * @name config
  * @desc Define valid application routes
  */
    function config($routeProvider) {
      $routeProvider.when('/accounts/users', {
          templateUrl: '/static/templates/users/user_all.html',
          controller: 'UserListController',
          controllerAs: 'ul'
        });
    }
})();
