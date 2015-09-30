/**
* Author : @mamun0024
* UserListController
* @namespace djangoUser.users.controllers
*/
(function () {
  'use strict';

  angular
    .module('djangoUser.users.controllers')
    .controller('UserListController', UserListController);

  UserListController.$inject = ['$location', '$scope', 'users', '$http'];

  /**
  * @namespace UserListController
  */
  function UserListController($location, $scope, users, $http) {
    var ul = this;
    $http.get('/accounts/users/api/userList').success(function(data) {
        $scope.userData = data;
    });
    $http.get('/accounts/users/api/userType').success(function(data) {
        $scope.userType = data;
    });
  }
})();