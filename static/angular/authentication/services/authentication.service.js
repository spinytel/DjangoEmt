/**
* Authentication
* @namespace djangoEMT.authentication.services
*/
(function () {
  'use strict';

  angular
    .module('djangoEMT.authentication.services')
    .factory('Authentication', Authentication);

  Authentication.$inject = ['$location', '$cookies', '$http'];

  /**
  * @namespace Authentication
  * @returns {Factory}
  */
  function Authentication($location, $cookies, $http) {
    /**
    * @name Authentication
    * @desc The Factory to be returned
    */
    var Authentication = {
        login: login,
        logout: logout,
        getAuthenticatedAccount: getAuthenticatedAccount,
        isAuthenticated: isAuthenticated,
        setAuthenticatedAccount: setAuthenticatedAccount,
        unauthenticate: unauthenticate
    };

    return Authentication;

    ////////////////////


    /**
    * @name login
    * @desc Try to log in with email `email` and password `password`
    * @param {string} email The email entered by the user
    * @param {string} password The password entered by the user
    * @returns {Promise}
    * @memberOf djangoEMT.authentication.services.Authentication
    */
    function login(email, password) {
        var data = 'email='+email+'&password=' +password;
        $http({
            method: 'POST',
            url: '/accounts/login/',
            data: data,
            headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        })
        .success(function(data, status, headers, config) {
            Authentication.setAuthenticatedAccount(data.data);
            $location.url('/accounts/users/');
        })
        .error(function(data, status, headers, config) {
            console.error('Epic failure!');
        })
    }


    /**
    * @name logout
    * @desc Try to log the user out
    * @returns {Promise}
    * @memberOf djangoEMT.authentication.services.Authentication
    */
    function logout() {
        $http({
            method: 'POST',
            url: '/accounts/logout/',
            headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        })
        .success(function(data, status, headers, config) {
            Authentication.unauthenticate();
            $location.url('/accounts/login');
        })
        .error(function(data, status, headers, config) {
            console.error('Epic failure!');
        })
    }


    /**
    * @name getAuthenticatedAccount
    * @desc Return the currently authenticated account
    * @returns {object|undefined} Account if authenticated, else `undefined`
    * @memberOf djangoEMT.authentication.services.Authentication
    */
    function getAuthenticatedAccount() {
        if (!$cookies.authenticatedAccount) {
        return;
        }
        return JSON.parse($cookies.authenticatedAccount);
    }


    /**
    * @name isAuthenticated
    * @desc Check if the current user is authenticated
    * @returns {boolean} True is user is authenticated, else false.
    * @memberOf djangoEMT.authentication.services.Authentication
    */
    function isAuthenticated() {
        return !!$cookies.authenticatedAccount;
    }


    /**
    * @name setAuthenticatedAccount
    * @desc Stringify the account object and store it in a cookie
    * @param {Object} user The account object to be stored
    * @returns {undefined}
    * @memberOf djangoEMT.authentication.services.Authentication
    */
    function setAuthenticatedAccount(account) {
        $cookies.authenticatedAccount = JSON.stringify(account);
    }


    /**
    * @name unauthenticate
    * @desc Delete the cookie where the user object is stored
    * @returns {undefined}
    * @memberOf djangoEMT.authentication.services.Authentication
    */
    function unauthenticate() {
        delete $cookies.authenticatedAccount;
    }
  }
})();