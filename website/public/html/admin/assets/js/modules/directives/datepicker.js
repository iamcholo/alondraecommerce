define(['angular','jquery'],function(angular,jquery){

      'use strict';

    angular.module('datepicker', []).

    directive('datepicker', function () {
        return {
         
            
            replace: true,
            scope : {
              ngModel : '=',
            },            

            templateUrl: '/admin/assets/js/modules/templates/includes/datepicker.html',
            link: function($scope, elem, attr, ctrl) {
                jquery('#datetimepicker10').datetimepicker({
                    viewMode: 'years',
                    format: 'YYYY-MM-DD H:mm:ss'
                }).on("dp.change", function (e) {
                    $scope.ngModel  = jquery('#datetimepicker10 input').val();
                });
            },
            controller: ['$scope','$timeout', function ($scope,$timeout) {
               
            
            }]

        }
    });

  
});
