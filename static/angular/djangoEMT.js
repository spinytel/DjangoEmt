(function () {
  'use strict';

  angular
    .module('djangoEMT', [
      'djangoEMT.config',
      'djangoEMT.routes',
      'djangoEMT.authentication',
      'djangoEMT.layout'
    ]);

  angular
    .module('djangoEMT.config', []);

  angular
    .module('djangoEMT.routes', ['ngRoute']);

  angular
    .module('djangoEMT')
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
