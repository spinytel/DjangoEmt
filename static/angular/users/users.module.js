/**
* Author : @mamun0024
*/
(function () {
  'use strict';

  angular
    .module('djangoUser.users', [
      'djangoUser.users.controllers',
      'djangoUser.users.services'
    ]);

  angular
    .module('djangoUser.users.controllers', []);

  angular
    .module('djangoUser.users.services', ['ngCookies']);
})();
