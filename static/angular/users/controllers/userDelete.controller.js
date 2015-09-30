/**
* Author : @mamun0024
* UserDeleteController
* @namespace djangoUser.users.controllers
*/
(function () {
  'use strict';

  angular
    .module('djangoUser.users.controllers')
    .controller('UserDeleteController', UserDeleteController);

  UserDeleteController.$inject = ['$location', '$scope', 'users', '$http'];

  /**
  * @namespace UserDeleteController
  */
  function UserDeleteController($location, $scope, users, $http) {
    var ud = this;

    ud.user_delete = user_delete;

    function user_delete(id) {
      $http({
            method: 'POST',
            url: '/accounts/users/'+id+'/delete',
            headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        })
        .success(function(data, status, headers, config) {
            $location.url('/accounts/users/');
        })
        .error(function(data, status, headers, config) {
            console.error('Epic failure!');
        })
    }
  }
})();