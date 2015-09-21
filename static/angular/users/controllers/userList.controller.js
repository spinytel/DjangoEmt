/**
* UserListController
* @namespace djangoUser.users.controllers
*/
(function () {
  'use strict';

  angular
    .module('djangoUser.users.controllers')
    .controller('UserListController', UserListController);

  UserListController.$inject = ['$location', '$scope', 'users'];

  /**
  * @namespace UserListController
  */
  function UserListController($location, $scope, users) {
    var ul = this;


  }
})();