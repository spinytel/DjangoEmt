/**
* Author : @mamun0024
*/
(function () {
  'use strict';

  angular
    .module('djangoUser', [
      'djangoUser.config',
      'djangoUser.routes',
      'djangoUser.users'
    ]);

  angular
    .module('djangoUser.config', []);

  angular
    .module('djangoUser.routes', ['ngRoute']);

  angular
    .module('djangoUser')
    .run(run);

  run.$inject = ['$http'];

  /**
  * @name run
  * @desc Update xsrf $http headers to align with Django's defaults
  */
  function run($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
  }
})();
