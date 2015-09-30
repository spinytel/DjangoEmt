/**
* Author : @mamun0024
* Users
* @namespace djangoUser.users.services
*/
(function () {
  'use strict';

  angular
    .module('djangoUser.users.services')
    .factory('users', users);

  users.$inject = ['$location','$cookies', '$http'];

  /**
  * @namespace Users
  * @returns {Factory}
  */
  function users($location, $cookies, $http) {
    /**
    * @name Users
    * @desc The Factory to be returned
    */
    var users = {
      user_add:user_add,
      user_edit:user_edit
    };

    return users;

    function user_add(is_admin, username, email, password, confirm_password) {
        if(is_admin == null){
            toastr.warning('User Type Selection Required.', "Warning !!!");
            return false;
        }else if(username == null){
            toastr.warning('Name Required.', "Warning !!!");
            return false;
        }else if(email == null){
            toastr.warning('Email Required.', "Warning !!!");
            return false;
        }else if(password == null){
            toastr.warning('Password Required.', "Warning !!!");
            return false;
        }else if(confirm_password == null){
            toastr.warning('Confirm Password Required.', "Warning !!!");
            return false;
        }else if(password != confirm_password){
            toastr.warning('Password Mismatch.', "Warning !!!");
            return false;
        }

      var data = 'is_admin='+is_admin+'&username=' +username+'&email=' +email+'&password=' +password+'&confirm_password=' +confirm_password;
        $http({
            method: 'POST',
            url: '/accounts/users/create/',
            data: data,
            headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        })
        .success(function(data, status, headers, config) {
            $location.url('/accounts/users/');
            console.log(config);
        })
        .error(function(data, status, headers, config) {
            console.error('Epic failure!');
        })
    }

    function user_edit(is_admin, username, email, user_pre_id) {
        if(is_admin == null){
            toastr.warning('User Type Selection Required.', "Warning !!!");
            return false;
        }else if(username == null){
            toastr.warning('Name Required.', "Warning !!!");
            return false;
        }else if(email == null){
            toastr.warning('Email Required.', "Warning !!!");
            return false;
        }

        if(is_admin == 0){
            is_admin = 'False';
        }else{
            is_admin = 'True';
        }

        var data = [];
        /*data = { 'is_admin': is_admin, 'username': username, 'email': email };*/
        data = 'is_admin='+is_admin+'&username=' +username+'&email=' +email;

        var url = '/accounts/users/api/'+user_pre_id+'/edit';

        $http({
            method: 'POST',
            url: url,
            data: data,
            headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-CSRFToken': $cookies['csrftoken']}
        })
        .success(function(data, status, headers, config) {
            $location.url('/accounts/users/');
        })
        .error(function(data, status, headers, config) {
            console.error(config);
        })
    }

  }
})();