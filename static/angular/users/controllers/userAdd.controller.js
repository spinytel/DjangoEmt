/**
* Author : @mamun0024
* UserAddController
* @namespace djangoUser.users.controllers
*/
(function () {
  'use strict';

  angular
    .module('djangoUser.users.controllers')
    .controller('UserAddController', UserAddController);

  UserAddController.$inject = ['$location', '$scope', 'users', '$http'];

  /**
  * @namespace UserAddController
  */
  function UserAddController($location, $scope, users, $http) {
    var ua = this;
    ua.user_add = user_add;

    function user_add() {
      users.user_add(ua.is_admin, ua.username, ua.email, ua.password, ua.confirm_password);
    }
  }
})();