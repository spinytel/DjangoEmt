/**
* Users
* @namespace djangoUser.users.services
*/
(function () {
  'use strict';

  angular
    .module('djangoUser.users.services')
    .factory('users', users);

  users.$inject = ['$location', '$http'];

  /**
  * @namespace Users
  * @returns {Factory}
  */
  function users($location, $http) {
    /**
    * @name Users
    * @desc The Factory to be returned
    */
    var users = {
      user_add:user_add
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
        })
        .error(function(data, status, headers, config) {
            console.error('Epic failure!');
        })
    }

  }
})();