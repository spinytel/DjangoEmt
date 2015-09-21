(function () {
  'use strict';

  angular
    .module('djangoEMT.authentication', [
      'djangoEMT.authentication.controllers',
      'djangoEMT.authentication.services'
    ]);

  angular
    .module('djangoEMT.authentication.controllers', []);

  angular
    .module('djangoEMT.authentication.services', ['ngCookies']);
})();
