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
    };

    return users;

  }
})();