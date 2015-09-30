/**
* Author : @mamun0024
*/
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
        }).when('/accounts/users/create', {
          templateUrl: '/static/templates/users/user_create.html',
          controller: 'UserAddController',
          controllerAs: 'ua'
        }).when('/accounts/users/:user_id/edit', {
          templateUrl: '/static/templates/users/user_edit.html',
          controller: 'UserEditController'
        });
    }
})();
