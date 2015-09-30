/**
* Author : @mamun0024
* UserEditController
* @namespace djangoUser.users.controllers
*/
(function () {
  'use strict';

  angular
    .module('djangoUser.users.controllers')
    .controller('UserEditController', UserEditController);

  UserEditController.$inject = ['$location', '$scope', 'users', '$routeParams', '$http'];

  /**
  * @namespace UserEditController
  */
  function UserEditController($location, $scope, users, $routeParams, $http) {

    $scope.user_edit = user_edit;

    var user_id = $routeParams.user_id;
    window.location.href = '/accounts/users/'+user_id+'/edit/';

    $http({
        method: 'GET',
        url: '/accounts/users/api/'+user_id+'/userData',
        headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    })
    .success(function(data, status, headers, config) {
        $scope.is_admin = data["is_admin"];
        $scope.username = data["username"];
        $scope.email = data["email"];
        $scope.id = data["id"];
    })
    .error(function(data, status, headers, config) {
        console.error('Epic failure!');
    });

    $http.get('/accounts/users/api/userType').success(function(data) {
        $scope.userType = data;
    });

    function user_edit() {
        /*window.location = '/accounts/users/'+user_id+'/edit/';*/
      users.user_edit($scope.is_admin, $scope.username, $scope.email, $scope.id);
    }


  }
})();