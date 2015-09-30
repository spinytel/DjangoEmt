/**
* Author : @mamun0024
*/
(function () {
  'use strict';

  angular
    .module('djangoUser.config')
    .config(config);

  config.$inject = ['$locationProvider', '$interpolateProvider'];

  /**
  * @name config
  * @desc Enable HTML5 routing
  */
  function config($locationProvider, $interpolateProvider) {
    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
    $locationProvider.hashPrefix('!');

    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
  }
})();